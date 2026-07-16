# Repository Learning Guidelines

This repository is an interactive, from-scratch computer-science curriculum. Help the learner understand and implement each concept instead of completing exercises for them.

## General workflow

- Work on one problem or tightly related concept at a time.
- Before resuming, inspect the relevant source file and lesson to determine the learner's current position.
- Keep the current exercise in the track's main source file unless that exercise specifically teaches multiple files or packages.
- Put conceptual guides in the track's `lessons/` directory, not in its project overview README.
- Explain the mental model and the reason behind a correction, not only the final syntax.
- Do not replace the learner's solution merely because it could be written differently. Identify correctness issues and focused improvements.

## Verification

- Inspect the learner's current implementation before declaring a problem complete.
- Run the language-appropriate formatter, static checks, tests, and executable when available.
- Explain failures using the relevant source lines and execution flow.
- Advance only after the current problem behaves correctly.

## Progression

- Preserve completed lessons and supporting examples.
- When preparing the next problem, add one focused lesson under the appropriate `lessons/` directory.
- Leave the new exercise unsolved, with a clear task, expected behavior, and verification commands.
- Keep repository-wide instructions here. Put language- or directory-specific rules in a closer nested `AGENTS.md`.

## Git safety

- Review the working tree before staging.
- Preserve unrelated learner changes.
- Stage only the files confirmed to belong to the requested commit.
- Run relevant validation before committing or pushing.
