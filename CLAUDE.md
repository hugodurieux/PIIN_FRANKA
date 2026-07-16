# PINN Franka Pipeline — Master Context

## What this project is

A Master's research project building a pipeline that takes a robot's **URDF file as
input** and ends with a **trained, controllable robot**. Current focus: the Franka
Panda 7-DoF arm. The scientific contribution is defined **relative to the state of
the art in Liu et al. (2024)** — the project must prove the 4 novelties listed in
`goal.md`.

## The authoritative files (read these, in this order)

1. **goal.md** — the 4 novelties to prove. This is the north star. Every decision,
   every novelty kept from a paper, must serve one of these objectives.
2. **Step1_Indication.md** — everything done so far on stage 1 (the PINN) and the
   direction stage 1 must keep. The PINN model may change, but the principle holds.
3. **tracking/PROJECT_STATE.md** — the living map of the whole project (maintained
   by the project-tracker agent).
4. **SESSION.md** — state carried between sessions (maintained by session-scribe).

## The project in stages

- **Stage 1 (core, current):** PINN dynamics learning. Grey-box = analytical inverse
  dynamics (RNEA from URDF, via Pinocchio) + a learned, constrained, payload-conditioned
  torque residual. This is where the goal.md novelties live.
- **Stage 2:** Motion planning with **MoveIt2 (ROS2)**. Keep it simple — use standard
  MoveIt2, just enough to showcase the stage-1 contribution.
- **Stage 3:** A controller + connecting everything end-to-end. Keep it simple
  (computed-torque feedforward + PD on top of the learned model).
- **Stage 4 (optional):** Grabbing / grasping.

## Stage 1 architecture (do not break without instruction)

- Grey-box: tau_pred = RNEA(q, qdot, qddot) [white box] + tau_res(q, qdot, delta) [network]
- Input encoding: [sin(q), cos(q), qdot, delta] -> X in R^22
- Activations: **Mish or Softplus only — never ReLU** (smooth torques for the motors)
- Loss = MSE(tau_pred, tau_real) + augmented Lagrangian (torque limits + dissipativity)
- The RNEA baseline (pinocchio_baseline/) is NEVER modified — only tau_res is learned
- qddot is used ONLY offline during training, never in the 1 kHz control loop

## Franka Panda constants

- 7 joints; torque limits [87,87,87,87,12,12,12] Nm
- Max velocities [2.175,2.175,2.175,2.175,2.610,2.610,2.610] rad/s
- Target control rate: 1000 Hz; payloads tested: 0, 1, 3 kg

## The automated paper workflow

Run `/process-papers` to process every paper in `papers/inbox/`:
read -> extract -> evaluate vs goal.md -> write CSV -> implement KEEP novelties
(auto branch) -> validate physics -> update PROJECT_STATE.md -> move to
papers/processed/. The loop runs over all papers without stopping.
You refill papers/inbox/ with new papers yourself.

## Agent permissions (general)
- Code-touching agents -> always a feature branch, never main
- Paper-reading / supervising agents -> read only
- Branches are merged manually by the human after review

## Running project code (Python, ROS2, training)
- Claude may run project code directly: `python x.py`, `python -m training.train`,
  `pytest`, `ros2 launch`/`ros2 run`, etc. — no separate human authorization
  required. This was a stricter policy earlier in the project (hook-enforced);
  the human explicitly asked to lift it (2026-07-16) so Claude can drive
  multi-terminal ROS2/Isaac Sim workflows without relaying every command.
- Real limitation, not a policy one: Claude cannot see GUI windows (Isaac Sim's
  viewport, RViz). Visual verification of robot motion still needs the human —
  run headless/log-based checks (`ros2 topic echo`, checkpoints, exit codes)
  wherever possible, and ask the human to confirm anything that can only be
  judged visually.
- Still exercise normal judgment around expensive/long-running jobs (e.g. full
  GPU training runs) and anything that could command real hardware in the
  future — prefer reporting the plan and a quick sanity run before launching
  something large or irreversible, same as the general "Executing actions with
  care" guidance.

## Session state (auto-updated)
@SESSION.md
