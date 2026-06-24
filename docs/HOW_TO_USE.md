# Usage Guide — PINN Franka Pipeline

## Installation (once)

```bash
mkdir ~/pinn_franka && cd ~/pinn_franka && git init
unzip /path/pinn_agents_v7.zip -d .
# Replace the placeholders with your real files:
#   goal.md             <- your 4 objectives
#   Step1_Indication.md <- your stage-1 status
claude
```

Check inside Claude Code:
```
/agents     # should list 8 agents
/help       # /process-papers should appear in the commands
```

## The single command: /process-papers

This is the heart of the system. You drop papers, run one command, everything happens.

```bash
# 1. Put your papers (PDF or MD) into the inbox
cp ~/Downloads/*.pdf papers/inbox/
```

```
# 2. In Claude Code, run:
/process-papers
```

### What the command does, for EACH paper, automatically:
1. paper-extractor reads the paper and extracts the info
2. novelty-supervisor judges the novelties against goal.md
3. A row is appended to tracking/papers_review.csv
4. For each KEEP novelty: implementer codes it on an auto git branch
5. physics-validator audits the code
6. project-tracker updates tracking/PROJECT_STATE.md
7. The paper is moved to papers/processed/

The loop runs over ALL papers without stopping. At the end, a recap + SESSION.md
is updated. You refill papers/inbox/ with new papers whenever you want.

## Code execution is OFF by default
The implementer WRITES code but never RUNS it (a hook blocks Python execution).
After the loop, it lists the exact commands; you run them yourself.

## After the loop: your validation work

Novelties are coded on branches but NEVER merged automatically.
```bash
git branch                          # see the novelty/* branches
git checkout novelty/Liu2024-N1     # inspect
# if OK:
git checkout main && git merge novelty/Liu2024-N1
```

## End of session
```
Update SESSION.md
```
Next day, on startup, all context is reloaded automatically.

## The 8 agents
| Agent | Model | Role |
|-------|-------|------|
| paper-extractor | Sonnet | Reads a paper, writes the CSV |
| novelty-supervisor | Sonnet | Judges vs goal.md (read-only) |
| implementer | Opus | Codes KEEP novelties (auto branch) |
| physics-validator | Sonnet | Audits the code (read-only) |
| project-tracker | Sonnet | Keeps PROJECT_STATE.md up to date |
| data-pipeline | Sonnet | Generates datasets (Fourier + RNEA) |
| experiment-tracker | Haiku | Logs training runs |
| session-scribe | Haiku | Memory between sessions |

## Running an agent on its own (outside the loop)
```
Use data-pipeline to generate a 1kg dataset, 10 minutes
Use experiment-tracker to log the run models/run_X/
```
