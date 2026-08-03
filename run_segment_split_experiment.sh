#!/usr/bin/env bash
# =====================================================================
# Does the black box still beat the grey box when the split is honest?
#
#   bash run_segment_split_experiment.sh            # 3 seeds (recommended)
#   bash run_segment_split_experiment.sh 12345      # one specific seed
#   EPOCHS=2 bash run_segment_split_experiment.sh 1 # ~1 min smoke test
#
# THE QUESTION
# ------------
# The 2026-07-31 results say a black box of identical capacity is 28 % more
# accurate than the grey box (0.447 vs 0.624 Nm mean test RMSE). That was
# measured under training/splits.py, which draws a uniform permutation over
# INDIVIDUAL SAMPLES. The data is not i.i.d. samples: it is 30 continuous 5 s
# trajectories at 1 kHz. So every test sample has a near-duplicate 1 ms away
# in the training set.
#
# That leak is not neutral across the comparison. RNEA fits nothing and gains
# nothing from it. The grey box only has to learn a residual. The black box
# has to reconstruct inertia and gravity from data alone, so it gains most.
#
# The tell: training/dataset.py never loads qddot, so the black box's input is
# (q, qdot, delta) and it CANNOT represent the inertial torque M(q) qddot at
# all -- yet it won by 28 %. With only 30 trajectories, (q, qdot) nearly
# identifies trajectory and phase, so qddot is recoverable by memorisation.
#
# This script re-runs the comparison with --split_mode segment, which puts
# whole trajectories on one side of the split, removing that shortcut.
#
# WHAT COUNTS AS AN ANSWER
# ------------------------
# 80/10/10 over 30 groups leaves ~3 test trajectories. However many samples
# those contain, the effective sample size is small, so ONE SEED IS NOT A
# RESULT. The default runs three seeds; report mean and spread, and treat a
# gap smaller than the spread as "no measured difference".
#
# Whatever comes out goes in the report. If the black box still wins, that is
# the finding. Section 5.2 of the report (sec-res-partition) is written to be
# updated either way and currently states the measurement has not been run.
# =====================================================================

set -u -o pipefail

cd "$(dirname "$0")" || exit 1

# --- interpreter (same resolution order as run_experiments.sh) -------
if [ -n "${PYTHON:-}" ]; then
    PY="${PYTHON}"
elif [ -x "./.venv/bin/python" ]; then
    PY="./.venv/bin/python"
else
    PY="python3"
fi

DATA="data/isaac_0.0kg.h5 data/isaac_1.0kg.h5 data/isaac_3.0kg.h5"
EPOCHS="${EPOCHS:-200}"
ARCH="--hidden_dim 256 --n_hidden_layers 4 --activation mish"

SEEDS=("$@")
if [ "${#SEEDS[@]}" -eq 0 ]; then SEEDS=(12345 23456 34567); fi

STAMP="$(date +%Y%m%d_%H%M%S)"
RESULTS="results/segsplit_${STAMP}"

# --- preflight -------------------------------------------------------
echo "=== preflight ==="
for f in $DATA; do
    [ -f "$f" ] || { echo "MISSING: $f"; exit 1; }
done
"$PY" -c "import torch, h5py" 2>/dev/null \
    || { echo "FAIL: $PY lacks torch/h5py. Set PYTHON=... or use ./.venv"; exit 1; }
echo "interpreter: $PY"
echo "seeds      : ${SEEDS[*]}"
echo "epochs     : $EPOCHS"

# A short run is a machinery check, not a measurement -- and its output looks
# exactly like a measurement. The black box starts from noise while the grey
# box starts from RNEA, so a truncated run measures convergence SPEED, which
# the grey structure wins trivially and which is not the question. Mark it
# everywhere so the logs cannot be misread later.
SMOKE=0
if [ "$EPOCHS" -lt 50 ]; then
    SMOKE=1
    cat <<'WARN'

  #####################################################################
  ##  SMOKE TEST ONLY -- EPOCHS < 50. THE NUMBERS BELOW ARE NOT A     ##
  ##  RESULT AND MUST NOT BE REPORTED.                                ##
  ##                                                                  ##
  ##  The black box trains from scratch; the grey box inherits RNEA   ##
  ##  from epoch 0. A truncated run measures convergence speed, not   ##
  ##  accuracy, and flatters the grey box by construction.            ##
  ##                                                                  ##
  ##  This run checks the machinery only. Use EPOCHS=200 (default).   ##
  #####################################################################

WARN
fi

mkdir -p "$RESULTS"
{
    echo "date:    $(date -Iseconds)"
    echo "python:  $($PY --version 2>&1)"
    echo "seeds:   ${SEEDS[*]}"
    echo "epochs:  $EPOCHS"
    [ "$SMOKE" -eq 1 ] && echo "STATUS:  SMOKE TEST (epochs < 50) -- NOT A RESULT"
    command -v nvidia-smi >/dev/null && nvidia-smi --query-gpu=name,memory.total \
        --format=csv,noheader
} > "$RESULTS/env.txt" 2>&1

# Verify boundary recovery BEFORE spending GPU time on it. If the segments
# cannot be recovered, everything downstream is meaningless.
echo
echo "=== segment recovery check ==="
# Segment RECOVERY is seed-independent; the split preview it prints is not.
# Pass the first seed so the preview matches what the first run will actually
# use -- printing the default partition next to a run using another seed reads
# as a mismatch and invites exactly the wrong conclusion.
"$PY" -m training.segment_splits --data $DATA --split_seed "${SEEDS[0]}" 2>&1 \
    | tee "$RESULTS/p0_segment_check.log"
# shellcheck disable=SC2181
if [ "${PIPESTATUS[0]}" -ne 0 ]; then
    echo "FAIL: could not recover trajectory segments. Stopping."
    exit 1
fi

# --- per seed --------------------------------------------------------
for SEED in "${SEEDS[@]}"; do
    echo
    echo "======================================================="
    echo "  SEED $SEED"
    echo "======================================================="

    GREY_TAG="segsplit-greybox-s${SEED}"
    MLP_TAG="segsplit-mlp-s${SEED}"
    COMMON="--data $DATA --epochs $EPOCHS $ARCH \
            --split_mode segment --split_seed $SEED"

    echo "--- grey box (seed $SEED) ---"
    # shellcheck disable=SC2086
    "$PY" -m training.train $COMMON --use_friction_net --tag "$GREY_TAG" 2>&1 \
        | tee "$RESULTS/s${SEED}_greybox.log"

    echo "--- black box, --no_rnea (seed $SEED) ---"
    # shellcheck disable=SC2086
    "$PY" -m training.train $COMMON --no_rnea --tag "$MLP_TAG" 2>&1 \
        | tee "$RESULTS/s${SEED}_mlp.log"

    GREY_DIR="$(ls -dt models/run_* | while read -r d; do
        grep -ql "\"tag\": \"$GREY_TAG\"" "$d/config.json" 2>/dev/null \
            && { echo "$d"; break; }; done)"
    MLP_DIR="$(ls -dt models/run_* | while read -r d; do
        grep -ql "\"tag\": \"$MLP_TAG\"" "$d/config.json" 2>/dev/null \
            && { echo "$d"; break; }; done)"

    if [ -z "$GREY_DIR" ] || [ -z "$MLP_DIR" ]; then
        echo "FAIL: could not locate run dirs for seed $SEED"
        echo "  grey='$GREY_DIR' mlp='$MLP_DIR'"
        exit 1
    fi
    echo "grey box  -> $GREY_DIR"
    echo "black box -> $MLP_DIR"

    echo "--- comparison on the SEGMENT test split (seed $SEED) ---"
    # eval_baselines verifies each checkpoint's config.json records this same
    # split_mode/split_seed, and refuses to run otherwise.
    # shellcheck disable=SC2086
    "$PY" -m evaluation.eval_baselines \
        --data $DATA \
        --split_mode segment --split_seed "$SEED" \
        --compare "rnea=" "greybox=$GREY_DIR" "mlp=$MLP_DIR" \
        --latex --json_out "$RESULTS/s${SEED}_comparison.json" 2>&1 \
        | tee "$RESULTS/s${SEED}_comparison.log"
done

# --- summary ---------------------------------------------------------
echo
echo "======================================================="
echo "  DONE -- results in $RESULTS/"
echo "======================================================="
echo
echo "Mean test RMSE per seed (grep from the comparison JSONs):"
for SEED in "${SEEDS[@]}"; do
    f="$RESULTS/s${SEED}_comparison.json"
    [ -f "$f" ] || continue
    echo "  seed $SEED:"
    grep -E '"kind"|"mean_rmse"' "$f" | paste - - | sed 's/^/    /'
done
echo
echo "Compare against the SAMPLE-split numbers (results/20260731_164630/):"
echo "    rnea 1.456   greybox 0.624   mlp 0.447   -> black box ahead by 28 %"
echo
if [ "$SMOKE" -eq 1 ]; then
    cat <<'WARN'
  #####################################################################
  ##  REMINDER: SMOKE TEST (EPOCHS < 50). DISCARD THESE NUMBERS.      ##
  ##  They show the machinery runs. They do not answer the question.  ##
  #####################################################################
WARN
    exit 0
fi

echo "Read the spread across seeds before concluding anything. A gap smaller"
echo "than the seed-to-seed spread is not a measured difference."
echo
echo "Then update school_report/rapport/main.tex section sec-res-partition,"
echo "which currently states this measurement has not been run."
