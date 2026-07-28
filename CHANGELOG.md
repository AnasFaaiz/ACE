# Changelog

## [0.2.0] - 2026-07-28
### Added
- `acego <nickname>` shell function for instant project navigation
- `ace shell-init [--install]` to install or print the function
- `ace --version`
- Textual TUI dashboard (`ace tui`)
- Backup system (`ace backup`)

### Changed
- Replaced `install.sh` with pip/pipx installation

### Fixed
- `news`, `save`, and `schedule` commands were silently no-ops
- `ace project go` now exits nonzero on failure
