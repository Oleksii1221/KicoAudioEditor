# KAE Architecture

KAE is intentionally split into a small native desktop shell and testable core services.

## Layers

- `kae.core.metadata`: audio metadata reading, writing, artwork handling, and JSON import/export.
- `kae.core.settings`: persisted app preferences and recent files.
- `kae.core.i18n`: runtime UI labels for supported languages.
- `kae.ui`: PySide6 windows, dialogs, widgets, and theme loading.

## Branch Policy

- `dev`: active implementation work.
- `master`: release-ready state only after explicit approval.

## Supported Languages

- Ukrainian
- English
- Japanese
- Italian
- Polish
