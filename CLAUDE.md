# Project: AI-Assisted Box Selection System (Django)

## Purpose
This project is a small Django-based hiring assignment. It recommends the most suitable shipping box for a given e-commerce order (a list of products) by optimizing for physical fit and cost.

## Assignment Requirements (Implementation Drivers)
- Provide a clear, functional Django system.
- Provide a REST-like endpoint to calculate the best box.
- Maintain human-readability and clearly demonstrate human decision-making.
- Keep dependencies minimal (default SQLite, simple Django views).
- Final deliverables: GitHub repo, README.md, AI_USAGE.md, chat transcript, test cases, and test run outputs.

## Development Guidelines
- **Simplicity First**: Avoid unnecessary packages, abstractions, or design patterns unless strictly necessary.
- **TDD (Test-Driven Development)**: Write tests for core algorithms before hooking them into Django views.
- **Documentation as Code**: Keep all AI usage and decision-making documented in markdown files as we progress.

## AI Coding Agent Rules
- **No Unprompted Execution**: Do not write code or run commands without explicit approval from the user.
- **Explain Tradeoffs**: Always explain the "why" and wait for the user to make the decision.
- **No Hallucinated Requirements**: Stick strictly to the provided assignment text.
- **No Git Commands**: Do not run any git commands, as the environment is strictly non-git per global rules.
- **No Attribution**: Never add AI-authorship attributions (e.g., "Authored by Claude") to code, commits, or docs.

## Project Directory Map
```
/
├── CLAUDE.md          # Global AI instructions and project rules
├── CONTEXT.md         # Current state and architectural decisions
├── REFERENCE.md       # Domain concepts and terminology
├── core/              # Main Django project settings (to be created)
└── boxes/             # Main Django app for packing logic (to be created)
    └── CONTEXT.md     # Local context for packing algorithms
```

## Naming Conventions
- Variables/Functions: `snake_case`
- Classes: `PascalCase`
- Box dimensions: Always ordered `length, width, height` internally for consistency, though rotation will sort them largest-to-smallest.