# PostgreSQL Progress

Timezone: **Asia/Kolkata (IST)**

## How Timing Works

- **Started** means the checkpoint was created and given to the learner.
- **Completed** means Codex reviewed the exercise and verified that it works.
- **Wall time** is the difference between those timestamps.
- Wall time includes sleep, breaks, and time spent on other work.

Wall time is used for rough prediction. Obvious overnight or long idle gaps are
kept in the history but excluded from the typical-duration calculation.

## Checkpoint Times

| # | Checkpoint | Status | Started | Completed | Wall time |
|---|---|---|---|---|---|
| 01 | SQL file, CLI, and first table | Complete | 2026-07-26 06:06 IST | 2026-07-27 02:46 IST | 20h 40m* |
| 02 | Insert and read rows | Complete | 2026-07-27 02:46 IST | 2026-07-27 03:18 IST | 32m |
| 03 | Protect valid data | Complete | 2026-07-27 03:19 IST | 2026-07-27 03:39 IST | 20m |
| 04 | Filter rows | Complete | 2026-07-27 03:39 IST | 2026-07-27 03:51 IST | 12m |
| 05 | Sort and limit results | Complete | 2026-07-27 23:19 IST | 2026-07-27 23:36 IST | 17m |
| 06 | Missing values | Complete | 2026-07-27 23:38 IST | 2026-07-27 23:50 IST | 12m |
| 07 | Change and remove rows safely | Complete | 2026-07-28 04:53 IST | 2026-07-28 05:10 IST | 17m |
| 08 | Summarize data | Complete | 2026-07-28 11:11 IST | 2026-07-28 11:23 IST | 12m |
| 09 | Summarize groups | Complete | 2026-07-28 11:26 IST | 2026-07-28 11:44 IST | 18m |
| 10 | Model relationships | Complete | 2026-07-30 13:50 IST | 2026-07-30 14:16 IST | 26m |
| 11 | Combine matching rows | Complete | 2026-07-30 21:55 IST | 2026-07-30 22:12 IST | 17m |
| 12 | Preserve unmatched rows | Complete | 2026-07-30 22:13 IST | 2026-07-30 22:23 IST | 10m |
| 13 | Design relational schemas | Not started | — | — | — |
| 14 | Make changes atomic | Not started | — | — | — |
| 15 | Make reads faster | Not started | — | — | — |
| 16 | Understand query execution | Not started | — | — | — |
| 17 | Prepare queries for applications | Not started | — | — | — |
| 18 | Raw SQL checkpoint | Not started | — | — | — |

\* Checkpoint 01 crossed an overnight/idle period, so it is excluded from the
typical-duration calculation.

## Current Estimate

- Completed: **12 of 18**
- Remaining: **6**
- Current estimate: **6–13 study hours**
- Confidence: **Low to medium**, because the completed same-session
  checkpoints are still introductory and later relational topics will take
  longer.

The estimate will be recalculated after each completed checkpoint. It should
become meaningfully more accurate after checkpoints 04–06.
