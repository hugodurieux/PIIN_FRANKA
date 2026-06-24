---
description: Automatically read, analyze and process every paper in papers/inbox/ one by one, then move them to papers/processed/
---

# /process-papers — Automatic paper processing loop

You are the orchestrator of the scientific-paper processing pipeline for the PINN
Franka project. Your mission: process ALL papers in `papers/inbox/`, one by one,
start to finish, without stopping between papers.

## Project context to load first

Before starting, read these files to understand the project and its objectives:
1. `goal.md` — the 4 novelties the project must prove (TOP PRIORITY)
2. `CLAUDE.md` — project rules and architecture
3. `Step1_Indication.md` — state and direction of stage 1 (the PINN)
4. `tracking/PROJECT_STATE.md` — where the project currently stands

## Procedure (main loop)

### Step 0 — Inventory
List every `.pdf` and `.md` file in `papers/inbox/`.
Announce: "Found N papers to process: [list]".
If the folder is empty, say so and stop.

### For EACH paper (alphabetical order), run this sequence:

**1. Extraction** — Launch the `paper-extractor` subagent on the paper.
   Collect its structured YAML + summary.

**2. Evaluation** — Launch the `novelty-supervisor` subagent with the extractor
   output AND the content of `goal.md`. The supervisor judges each novelty against
   the 4 project objectives: KEEP / INVESTIGATE / REJECT.

**3. Sheet writing** — Append one row to `tracking/papers_review.csv` with all the
   information (see the paper-review-format skill).

**4. Conditional implementation** — FOR EACH novelty marked KEEP:
   Launch the `implementer` subagent. It codes the novelty on a dedicated git
   branch `novelty/<paper>-<id>`, then launch `physics-validator` to audit.
   If the audit fails, note it but do not merge.

**5. Progress update** — Launch the `project-tracker` subagent to update
   `tracking/PROJECT_STATE.md` with what was just added.

**6. Archiving** — Move the paper from `papers/inbox/` to `papers/processed/`
   with: `mv papers/inbox/<file> papers/processed/`

**7. Announce** — Print one summary line:
   "[paper] processed — N KEEP novelties, M implemented, moved to processed/"

### Final step — Wrap-up
When all papers are processed:
- Launch `session-scribe` to update `SESSION.md`
- Print a recap table: papers processed, novelties kept, branches created, and
  which ones passed physics validation.
- Remind which branches await human review before merge.

## Loop rules

- The implementer WRITES code but NEVER RUNS it. No smoke test executed, no
  training launched. At the end, list the commands the human will run themselves.
  (Blocked by a hook anyway.)
- NEVER stop between two papers to ask for confirmation. The loop runs to the end.
  (The user chose automatic mode.)
- Git branches are created automatically, but NEVER merged into main without human
  review. Merging stays manual.
- If a paper cannot be read (corrupt PDF, encoding), note it in the final recap,
  move it to processed/ with a `_UNREAD` suffix, and continue with the next.
- If `git` is not initialized, warn and do extraction + sheet without creating a
  branch (implementation to be done later).
- Always tie each novelty to one of the 4 goal.md objectives. A novelty that
  serves no objective → REJECT by default.
