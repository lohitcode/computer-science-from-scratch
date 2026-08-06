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
| 13 | Design relational schemas | Complete | 2026-08-02 08:04 IST | 2026-08-02 09:19 IST | 1h 15m |
| 14 | Make changes atomic | Complete | 2026-08-03 15:23 IST | 2026-08-03 16:28 IST | 1h 05m |
| 15 | Make reads faster | Complete | 2026-08-03 23:45 IST | 2026-08-04 00:03 IST | 18m |
| 16 | Understand query execution | Complete | 2026-08-04 08:37 IST | 2026-08-04 08:59 IST | 22m |
| 17 | Prepare queries for applications | Complete | 2026-08-06 08:05 IST | 2026-08-06 08:23 IST | 18m (+ Stage A: 23m) |
| 18 | Raw SQL checkpoint | Complete | 2026-08-06 08:25 IST | 2026-08-06 16:49 IST | 8h 24m* |

\* Checkpoint 01 crossed an overnight/idle period, so it is excluded from the
typical-duration calculation. Checkpoint 18 included breaks; its four reset
stage timers totalled 2h 30m.

## Current Estimate

- Completed: **18 of 18**
- Remaining: **0**
- Raw PostgreSQL track status: **Complete**
- Next track: connect the Go HTTP server to PostgreSQL, introduce versioned
  migrations, configure SQLC, and generate the first type-safe Go methods.

Checkpoint 18 proved the complete raw-SQL foundation through schema design,
constraints, joins, transactions, indexes, query-plan interpretation, and
application-shaped parameterized queries.
