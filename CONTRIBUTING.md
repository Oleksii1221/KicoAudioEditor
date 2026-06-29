# Contributing

KAE uses a simple branch policy:

- `dev` is the working branch for implementation.
- `master` is release-ready only.

Before opening a pull request, run:

```powershell
pytest
ruff check .
```

Keep changes focused, avoid unrelated refactors, and include tests for core metadata behavior when possible.
