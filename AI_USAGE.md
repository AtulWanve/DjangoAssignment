# AI Usage Document

## 1. Which AI tool(s) you used
This project was developed with the assistance of **Claude Code** (powered by Anthropic's Claude models), acting as an autonomous CLI coding agent within the terminal environment.

## 2. The prompts you gave
The development was split into distinct, user-approved phases. Major prompts included:
- **Initial Analysis Request:** Asked Claude to analyze the assignment markdown, provide a concise interpretation of requirements, propose a minimum viable architecture, necessary models, a box-selection algorithm, required endpoints, and test cases, all without writing code.
- **Algorithm Deep Dive:** Requested an explanation of whether a simple volume heuristic could return false positives (providing 3 concrete counterexamples) and asked for a comparison between a simple heuristic and a realistic packing approach.
- **Implementation Planning:** Requested a practical breakdown of how the Greedy Space Partitioning algorithm would work (tracking empty space, rotation, overlap prevention) and a file-by-file implementation plan.
- **Architecture Confirmation:** Confirmed the decision to track only dimensions (not explicit X/Y/Z coordinates) and established documentation structure (`CLAUDE.md`, `CONTEXT.md`) before coding began.
- **Phase 1 Approval:** Authorized the initialization of the Django project and database models.
- **Interruption:** Interrupted Claude Code when it proceeded into Phase 2 without explicit approval.
- **Review and Course Correction:** Requested a code review to explain the implemented logic, identify assumptions/limitations, and find potential edge cases/bugs before running any tests.
- **Test execution:** Ran the final full test suite and Django checks, resulting in 13 tests passing and 0 Django system-check issues.

## 3. What output you accepted
- **Architecture:** A minimal, standard Django application using SQLite with two main models (`Box`, `Product`) and a single stateless API endpoint.
- **Algorithm:** The "Guillotine Split" (Greedy 3D Space Partitioning) approach tracking only the dimensions of empty spaces, acknowledging the limitation that it cannot merge adjacent fragmented spaces.
- **Code:** The Python implementation of `Space` and `Item` dataclasses, the packing logic in `boxes/packing.py`, the Django view in `boxes/views.py`, and the comprehensive unit tests in `boxes/tests.py`.

## 4. What output you rejected or modified
- **Autonomous Overreach:** During the transition between Phase 1 (Models) and Phase 2 (Algorithm), Claude Code's autonomous loop kicked in and began writing the packing algorithm and test files (`packing.py`, `tests.py`) and attempted to run the test suite without explicit user approval. This action was explicitly rejected, the test execution was blocked, and Claude was instructed to pause, review the written code, and wait for manual approval before proceeding.
- **Variable Naming:** Claude initially mapped the Django model's `length` attribute to the algorithm's `depth` attribute. This was flagged during code review and corrected to use `length` consistently across both the database and algorithm layers to prevent future cognitive overhead.

## 5. Any mistakes the AI made
- **False Alarm on Geometry:** Claude Code initially identified the split calculation as a bug during code review and later determined it was a false alarm after trying to mathematically prove it.
- **Over-eager Execution:** Claude Code proceeded into Phase 2 without explicit approval, and I interrupted it.

## 6. How you verified the final code
- **TDD / Unit Tests:** 13 unit tests were written to cover single-item fits, rotations, weight limits, and complex physical scenarios where total volume passes but physical dimensions fail (e.g., "Wasted Corner" and "Gridlock" scenarios).
- **Manual Review:** The Python code for the algorithm and the API view was explicitly paused and reviewed line-by-line by the human developer to ensure it matched the agreed-upon architecture.
- **System Checks:** Full `python manage.py test` and `python manage.py check` commands were run to verify 100% test passing and 0 framework configuration issues.