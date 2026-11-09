# Resources to arrange — 2026-11-09

**Current allocation, confirmed November 9:** owner handles Python/notebook execution checks,
design/writeup feedback and has full remote SSH access. Assistant handles football/statistical
research and internal review. External researchers are unavailable and are not a dependency.
The original suggestions below are optional if availability changes. Start with `START_HERE.md`;
the initial assistant SSH attempt reached the server but lacked accepted authentication.
Aim: improve football validity, statistical credibility and submission quality without additional spending. The owner has reported professor-provided remote RTX 5080 access (16 GiB VRAM) and a strong CPU. Connection, host RAM and resource availability remain unverified. These are requests the owner can make; no messages have been sent to anyone.

## Highest-value help
| Priority | Who/resource | Suggested ask | Result we need | Useful timing |
|---|---|---|---|---|
| 1 | American-football coach, WR coach or football analytics researcher | Two voluntary 30–45-minute feedback sessions | Is SLANT/OUT vs GO a sensible question? What does separation at throw measure? Which conclusions could a scout use, and what is missing? | First review by Nov 16; final story by Dec 7 |
| 2 | Statistics/econometrics professor or PhD researcher | 60–90 minutes reviewing the protocol, then 30 minutes on results | Critique player/game clustering, roughly 42/16 athlete samples, repeatability, selection, earlier 2025 exposure and uncertainty in prediction gain | Protocol before fits if possible; results by Nov 20 |
| 3 | Professor supplying compute | Stable account, resource inventory and documented availability | Host RAM, usable cores, free SSD, job limits, access method and end date; ability to save/resume jobs | Before remote jobs; preferably access through Dec 28 |
| 4 | Python/Jupyter-capable friend | Run the notebook from clean inputs; allow 1–2 hours initially | Missing files/dependencies, path assumptions, runtime/memory failures and exact reproduction of selected outputs | Early smoke run; full run Dec 1–14 |
| 5 | Design/technical-writing friend | Two 45–60-minute cold reads of the figures and draft | Unclear labels, small text, misleading colours, unexplained terms and whether the main decision is understandable | Nov 21–30 and Dec 1–7 |
| 6 | Biomechanics researcher or sports-science professor | 30–45-minute measurement review | Check signed acceleration, units, smoothing sensitivity and whether “turning capacity” is justified rather than merely a speed/path descriptor | During measurement audit |

One willing person with relevant expertise is more useful than several superficial reviewers. If no American-football expert is available locally, ask a professor for an introduction to a sports-analytics researcher or alumni coach. A general sports-science reviewer can assess kinematics but should not be presented as validating NFL route semantics.

## Remote-compute request to the professor
Suggested message for the owner to adapt:

> Thank you for the RTX 5080 access. For the NFL analytics project, the main jobs are CPU model
> fits and bootstrap validation. Could you share the machine's system RAM, CPU/core count,
> available SSD space, OS and access method, plus the allowed job duration and access end date?
> An isolated Python environment, a persistent working directory and permission to resume
> interrupted jobs would help. We can cap CPU/RAM usage and work within the available resources.

Useful preferences: **32–64 GiB system RAM**, **8–16 usable CPU cores**, **50–100 GB free SSD**. These are comfortable targets, not requirements to buy or upgrade hardware. The current raw data are approximately 2.2 GB and Parquets 382 MB; extra disk space is for environments, temporary query files, versions and checkpoints. The professor's current configuration may already be sufficient.

Confirm whether long jobs use a scheduler, a persistent shell session or a managed notebook; record sharing limits and data-working-directory permissions. Connection details can be configured securely when setting up access; do not put passwords, keys or tokens in project notes.

## Optional material
- Official data definitions and competition clarifications: resolve meaning/missingness before fitting models. Preserve source references for claims used in the writeup.
- Lawfully accessible route/Combine film, if already available through a coach or university: use a small, preselected set for interpretation and movement QC. Do not acquire a paid subscription for this plan or add film-derived outcome features without an amended protocol.
- A reliable internet connection and backup location for code, logs and permitted artifacts: more useful than additional GPU capacity when remote access is intermittent.

External data or collaboration must fit competition rules and the University-track constraints. Expert feedback does not automatically require adding someone to the team. Confirm what the rules permit before draft/data sharing or team changes; the owner handles legal/team UI actions.

## What each reviewer receives
Prepare compact review packets rather than asking someone to read the whole repository:
- Football: one-page question, annotated route trace and provisional evidence card.
- Statistics: frozen protocol, eligibility table and one model/evaluation table once available.
- Reproduction: notebook, dependency file, input instructions and expected output checks.
- Design/writing: rendered figures and a ≤2,000-word draft, with three specific readability questions.

Record feedback and resolutions in `reports/submission_checklist.md`. A review can improve the entry but cannot certify a prize. Extra hardware does not fix the small athlete sample.
