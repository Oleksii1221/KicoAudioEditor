# Release Process

KAE uses `dev` for active work and `master` for release-ready state.

1. Finish implementation on `dev`.
2. Run checks:

   ```bash
   pytest
   ruff check .
   ```

3. Build the Windows installer locally when on Windows:

   ```powershell
   packaging\windows\build-installer.ps1 -Version 0.1.0
   ```

4. Fast-forward `master` only when the release is approved.
5. Push a version tag such as `v0.1.0`.
6. Confirm the Release Packages workflow publishes Windows and Linux assets.
7. Confirm GitHub Pages returns HTTP 200.
