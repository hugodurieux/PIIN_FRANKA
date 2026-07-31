#!/usr/bin/env bash
# =====================================================================
# Every measurement the school report is currently missing, in order.
#
#   bash run_experiments.sh            # list the phases, run nothing
#   bash run_experiments.sh all        # run every phase in order
#   bash run_experiments.sh 1          # run one phase
#   bash run_experiments.sh 2 3 5      # run several
#
# Results land in results/<timestamp>/ : one log per phase, plus
# env.txt (GPU/CPU model) and timings.txt (wall clock per run). Those two
# files exist specifically to fill the report's two \acompleter markers in
# "Validation et resultats".
#
# WHY PHASE 1 IS NOT OPTIONAL
# ---------------------------
# training/splits.py introduced an 80/10/10 train/val/test partition. Before
# it, the split was 90/10 train/val, the reported RMSE was measured on the
# validation set, and the checkpoint was selected on that same set -- and
# controller/compute_error_bound.py derived epsilon_j, hence the live Kp/Kd,
# from it too. The existing checkpoints in models/ were trained under the old
# partition, so samples that are in today's TEST split were in their TRAINING
# set. Scoring them on today's test split would not be held out. Every number
# in the report has to come from models retrained in phase 1.
# =====================================================================

set -u -o pipefail

cd "$(dirname "$0")" || exit 1

DATA="data/isaac_0.0kg.h5 data/isaac_1.0kg.h5 data/isaac_3.0kg.h5"
EPOCHS="${EPOCHS:-200}"
# Held fixed across every run so the comparisons are attributable to the
# structure under test and not to capacity or budget.
ARCH="--hidden_dim 256 --n_hidden_layers 4 --activation mish"

STAMP="$(date +%Y%m%d_%H%M%S)"
RESULTS="results/${STAMP}"

usage() {
    cat <<'USAGE'
Phases
------
 1  Retrain the grey-box reference on the 80/10/10 split.       ~ the long one
      Produces the model every later phase compares against.
      Also: --use_friction_net, matching the current reference run.

 2  RNEA-only baseline. No training, no GPU, seconds.
      Fills the "RNEA seul" row of the report's baseline table.

 3  Black-box baseline (--no_rnea): the network predicts the whole torque.
      Fills the "MLP direct" row. Same arch/budget as phase 1.

 4  Spatial-encoding ablation (--encoding raw): [q,qdot,delta] instead of
      [sin q, cos q, qdot, delta]. The report's limitations section says
      this ablation is expected by reviewers and has never been run.

 5  Comparison table over phases 1-4 on the SAME test split, and emit the
      LaTeX table body ready to paste into the report.

 6  Recompute the Lyapunov error bound epsilon_j on the TEST split for the
      phase-1 model, then update controller/lyapunov_gains.py's
      DEFAULT_ERROR_BOUND. The current constant was computed the old way and
      is expected to be too small.

 7  FrictionNet ablation: phase-1 config WITHOUT --use_friction_net, to
      measure what the structurally-dissipative module actually buys.

 8  Data-efficiency curve (novelty N4): --max_samples 5000/25000/50000,
      against Liu et al.'s 25 000-sample benchmark.

Not covered here (closed-loop, needs the ROS2 stack running):
  payload conditioning in a real grasp, and the sim-to-sim fine-tuning
  validation. See tracking/STAGE4_TEST_PLAN.md and the notes at the bottom
  of this script.
USAGE
}

if [ "$#" -eq 0 ]; then usage; exit 0; fi

PHASES=("$@")
if [ "${1}" = "all" ]; then PHASES=(1 2 3 4 5 6 7 8); fi

mkdir -p "${RESULTS}" || exit 1
echo "Results -> ${RESULTS}"

# --- environment capture: fills the report's GPU/CPU \acompleter ---
{
    echo "date        : $(date -Is)"
    echo "host        : $(hostname)"
    echo "git commit  : $(git rev-parse --short HEAD 2>/dev/null)"
    echo "git branch  : $(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
    echo "epochs      : ${EPOCHS}"
    echo "arch        : ${ARCH}"
    echo "data        : ${DATA}"
    echo
    echo "--- CPU ---"
    lscpu 2>/dev/null | grep -E 'Model name|^CPU\(s\)|Thread|Core' || echo "lscpu unavailable"
    echo
    echo "--- GPU ---"
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv 2>/dev/null \
        || echo "no NVIDIA GPU visible (training will run on CPU)"
    echo
    echo "--- torch ---"
    python3 -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available())" 2>/dev/null \
        || echo "torch import failed"
} > "${RESULTS}/env.txt"
echo "Wrote ${RESULTS}/env.txt  (GPU/CPU model for the report)"

TIMINGS="${RESULTS}/timings.txt"
: > "${TIMINGS}"

# run <name> <command...>  -- times it, tees to a log, records wall clock
run() {
    local name="$1"; shift
    local log="${RESULTS}/${name}.log"
    echo
    echo "======================================================================"
    echo ">>> ${name}"
    echo ">>> $*"
    echo "======================================================================"
    local t0 t1 rc
    t0=$(date +%s)
    "$@" 2>&1 | tee "${log}"
    rc=${PIPESTATUS[0]}
    t1=$(date +%s)
    printf '%-28s %6d s   exit=%d\n' "${name}" "$((t1 - t0))" "${rc}" >> "${TIMINGS}"
    if [ "${rc}" -ne 0 ]; then
        echo "!!! ${name} FAILED (exit ${rc}). See ${log}"
        echo "!!! Later phases depend on it; stopping."
        exit "${rc}"
    fi
}

has_phase() { for p in "${PHASES[@]}"; do [ "$p" = "$1" ] && return 0; done; return 1; }

# Resolve the newest run directory carrying a given tag.
latest_run_with_tag() {
    local tag="$1" newest="" d
    for d in models/run_*/; do
        [ -f "${d}config.json" ] || continue
        if grep -q "\"tag\": \"${tag}\"" "${d}config.json" 2>/dev/null; then
            newest="${d%/}"
        fi
    done
    echo "${newest}"
}

# ---------------------------------------------------------------- phase 1
if has_phase 1; then
    run "p1_greybox_reference" \
        python3 -m training.train --data ${DATA} ${ARCH} \
            --epochs "${EPOCHS}" --use_friction_net \
            --tag greybox-reference
fi

# ---------------------------------------------------------------- phase 2
if has_phase 2; then
    run "p2_baseline_rnea" \
        python3 -m evaluation.eval_baselines --kind rnea --data ${DATA} \
            --json_out "${RESULTS}/p2_baseline_rnea.json"
fi

# ---------------------------------------------------------------- phase 3
if has_phase 3; then
    # No --use_friction_net: FrictionNet is a dissipative RESIDUAL module and
    # has no meaning when the network output is the whole torque.
    run "p3_baseline_mlp_direct" \
        python3 -m training.train --data ${DATA} ${ARCH} \
            --epochs "${EPOCHS}" --no_rnea \
            --tag baseline-mlp-direct
fi

# ---------------------------------------------------------------- phase 4
if has_phase 4; then
    run "p4_ablation_raw_encoding" \
        python3 -m training.train --data ${DATA} ${ARCH} \
            --epochs "${EPOCHS}" --use_friction_net --encoding raw \
            --tag ablation-raw-encoding
fi

# ---------------------------------------------------------------- phase 5
if has_phase 5; then
    GREY="$(latest_run_with_tag greybox-reference)"
    MLP="$(latest_run_with_tag baseline-mlp-direct)"
    RAW="$(latest_run_with_tag ablation-raw-encoding)"
    echo "grey-box reference : ${GREY:-MISSING}"
    echo "mlp direct         : ${MLP:-MISSING}"
    echo "raw encoding       : ${RAW:-MISSING}"
    if [ -z "${GREY}" ] || [ -z "${MLP}" ]; then
        echo "!!! phase 5 needs phases 1 and 3 to have run. Skipping."
    else
        ARGS=("rnea=" "greybox=${GREY}" "mlp=${MLP}")
        [ -n "${RAW}" ] && ARGS+=("greybox=${RAW}")
        run "p5_comparison_table" \
            python3 -m evaluation.eval_baselines --data ${DATA} --latex \
                --json_out "${RESULTS}/p5_comparison.json" \
                --compare "${ARGS[@]}"
    fi
fi

# ---------------------------------------------------------------- phase 6
if has_phase 6; then
    GREY="$(latest_run_with_tag greybox-reference)"
    if [ -z "${GREY}" ]; then
        echo "!!! phase 6 needs phase 1. Skipping."
    else
        run "p6_error_bound" \
            python3 -m controller.compute_error_bound \
                --run_dir "${GREY}" --data ${DATA}
        echo
        echo "ACTION REQUIRED: copy the p99.9 row from the log above into"
        echo "controller/lyapunov_gains.py :: DEFAULT_ERROR_BOUND, then update"
        echo "the epsilon_j / Kp / Kd table in the school report. The current"
        echo "constant [5.20 5.66 3.06 3.80 2.10 2.38 1.57] came from the old"
        echo "validation-set procedure and is expected to be too small."
    fi
fi

# ---------------------------------------------------------------- phase 7
if has_phase 7; then
    run "p7_ablation_no_frictionnet" \
        python3 -m training.train --data ${DATA} ${ARCH} \
            --epochs "${EPOCHS}" \
            --tag ablation-no-frictionnet
fi

# ---------------------------------------------------------------- phase 8
if has_phase 8; then
    for N in 5000 25000 50000; do
        run "p8_max_samples_${N}" \
            python3 -m training.train --data ${DATA} ${ARCH} \
                --epochs "${EPOCHS}" --use_friction_net --max_samples "${N}" \
                --tag "data-efficiency-${N}"
    done
fi

echo
echo "======================================================================"
echo "Done. ${RESULTS}/"
echo
cat "${TIMINGS}"
echo
cat <<'NEXT'
----------------------------------------------------------------------
To put these in the report (school_report/rapport/main.tex):

  * baseline table          <- phase 5's LaTeX block, replaces the
                               \acompleter{à mesurer} rows
  * GPU/CPU + training time <- results/<stamp>/env.txt and timings.txt,
                               replaces the two \acompleter markers in
                               "Validation et resultats"
  * per-joint RMSE table    <- phase 1's per_joint_test_rmse
  * epsilon_j / Kp / Kd     <- phase 6
  * encoding ablation       <- phase 4 vs phase 1, and delete the
                               "Ablation de l'encodage spatial non conduite"
                               bullet from the limitations list

STILL NOT COVERED -- both need the ROS2 stack live, not this script:

  A. Payload conditioning in a real grasp. delta is trained over
     {0,1,3} kg but ComputedTorquePDController.update_payload() has never
     been called during a pick. Needs the cube's MJCF density raised, the
     finger actuator kp raised with it, and GraspConfig.object_mass matched.
     Worked numbers are in tracking/STAGE4_TEST_PLAN.md.

  B. Sim-to-sim fine-tuning (novelty N3-Duong). training/fine_tune.py
     exists and has never been validated. The measured baseline it has to
     beat is the residual ablation already in the report: joint-5 bias
     -0.0337 rad and flange error 14.3 mm with the Isaac residual on.
     Fine-tune on MuJoCo data, then re-run that exact comparison.
----------------------------------------------------------------------
NEXT
