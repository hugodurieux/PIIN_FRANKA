---
name: paper-review-format
description: >
  Protocol for extracting structured information from scientific papers and writing
  it into tracking/papers_review.csv. Load this skill whenever a paper must be
  read, evaluated, or logged. Defines the exact CSV columns and the writing helper.
---

# Paper Review Format — Extraction Protocol

## The CSV file

Path: `tracking/papers_review.csv`

If it does not exist, create it with this exact header row:

```
date_processed,filename,title,authors,year,venue,summary_abstract,key_results,keywords,project_stage,relevance_score,potential_novelties,linked_goal,already_in_project,code_available,corroboration_value,notes
```

## Column definitions

| Column | What to write |
|--------|--------------|
| **date_processed** | Today's date (YYYY-MM-DD) |
| **filename** | Exact filename from papers/inbox/ |
| **title** | Full paper title |
| **authors** | First author last name + "et al." if >2 |
| **year** | Publication year |
| **venue** | Journal / conference / arXiv ID |
| **summary_abstract** | A 2-3 sentence summary IN YOUR OWN WORDS (never copy the abstract verbatim) |
| **key_results** | The main quantitative/qualitative results, 1-2 sentences |
| **keywords** | Semicolon-separated keywords USEFUL FOR THIS PROJECT (e.g. "dissipativity; LNN; friction; real-hardware") |
| **project_stage** | Which stage this paper informs: 1 (PINN), 2 (MoveIt2 motion planning), 3 (controller), 4 (grabbing). Can be multiple: "1;3" |
| **relevance_score** | 0-3: 0=none, 1=background, 2=potentially useful, 3=directly applicable to a goal.md objective |
| **potential_novelties** | Pipe-separated list "N1: desc \| N2: desc" — ideas extractable for OUR project |
| **linked_goal** | Which goal.md objective(s) each novelty serves, or "none" |
| **already_in_project** | yes / no |
| **code_available** | yes / no / partial — with URL if yes |
| **corroboration_value** | Pipe-separated list of existing design choices this paper independently validates: "aspect :: evidence (strength) [cite: yes/no → Section X]". Use "none" if paper provides no confirmation of existing choices. Example: "RNEA white-box :: Sutanto 2020 shows differentiable RNEA requires runtime gradients, confirming frozen-RNEA advantage (strong) [cite: yes → Section 3.2] \| Softplus diagonal :: Cholesky+Softplus is canonical for PD matrices (moderate) [cite: yes → Related Work]" |
| **notes** | Caveats, limitations, doubts (sim-only? gentle regime? etc.) |

## How to write a row (Python / csv — handles commas safely)

```python
import csv, os
from datetime import date

CSV = "tracking/papers_review.csv"
HEADER = ["date_processed","filename","title","authors","year","venue",
          "summary_abstract","key_results","keywords","project_stage",
          "relevance_score","potential_novelties","linked_goal",
          "already_in_project","code_available","corroboration_value","notes"]

def append_paper(row: dict):
    new_file = not os.path.exists(CSV)
    with open(CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        if new_file:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in HEADER})
```

Using csv.DictWriter is mandatory — it quotes fields containing commas so the
CSV never breaks. Never build CSV rows by string concatenation.

## Extraction rules

1. Read abstract, introduction, conclusion first; skim method for equations.
2. summary_abstract and key_results must be in your own words. NEVER copy text
   verbatim from the paper (copyright + it makes the sheet unusable).
3. For potential_novelties, think specifically about the 4 goal.md objectives
   and the 3 project stages. A novelty that serves no objective is not worth listing.
4. Be conservative on relevance_score: 3 only if implementable in stage 1 without
   architectural change.
5. project_stage: map honestly. A controller paper → stage 3. A motion planning
   or MoveIt2 paper → stage 2. A dynamics/PINN/friction paper → stage 1.
