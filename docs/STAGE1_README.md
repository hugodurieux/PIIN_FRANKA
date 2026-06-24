# Stage 1 — Grey-box PINN base (Franka Panda)

## Architecture

```
tau_pred(q, qdot, qddot, delta) = RNEA(q, qdot, qddot)      [white box, Pinocchio]
                                + tau_res(q, qdot, delta)    [GreyBoxNet]
```

The network learns ONLY the residual (friction, transmission, unmodeled effects).
RNEA is never learned or modified.

## Files

| File | Role |
|------|------|
| `network/constants.py` | Franka constants (torque limits, etc.) — single source |
| `network/grey_box_net.py` | Residual network (R^22 encoding, Mish/Softplus, R^7 output) |
| `pinocchio_baseline/rnea_wrapper.py` | RNEA via Pinocchio (+ payload delta injection) |
| `training/constraints.py` | Augmented Lagrangian: torque limits + **dissipativity** |
| `training/dataset.py` | HDF5 loader + synthetic dataset for testing |
| `training/train.py` | Training loop (Adam + MSE + AL) |

## Immediate test (no real data, no Pinocchio)

```bash
pip install torch numpy h5py
python -m training.train --synthetic --epochs 5
```

This trains the network on synthetic data (viscous + Coulomb friction) to check the
whole chain runs, without Pinocchio or real data. You should see val loss go down and
the dissipativity violation stay low.

> Note: code execution is blocked by a hook by default. Run the commands yourself.

## Test each module separately

```bash
python -m network.grey_box_net       # network smoke test
python -m training.constraints       # augmented Lagrangian smoke test
python -m training.dataset           # synthetic dataset smoke test
```

## Real training

1. Generate a dataset with the data-pipeline agent (or your real Franka) → `data/*.h5`
2. ```bash
   python -m training.train --data data/dataset_1kg_xxx.h5 --epochs 200
   ```
3. Weights are saved to `models/run_YYYYMMDD_HHMMSS/greybox_best.pt`
4. Log the run with the experiment-tracker agent

## Grounding in Liu et al. (2024)

| Element | What Liu does | What we do |
|---------|---------------|------------|
| Learned object | energy function (LNN) | torque residual on RNEA |
| Dissipation | dissipation term in the energy | **dissipativity constraint** (our novelty #2) |
| Acceleration qddot | avoided (RK4) | offline only, never at 1 kHz |
| Data | sinusoidal trajectories, filtering | Fourier excitation (data-pipeline agent) |
| Framework | JAX / dm-Haiku | PyTorch |
| Controller | PD + feedforward (stage 3) | computed-torque (stage 3) |

The dissipativity constraint (`constraint_dissipativity` in `constraints.py`) is the
bridge between Djeumou (constraint machinery) and Liu (stability guaranteed by
dissipation) — the core of what you contribute over the state of the art.
