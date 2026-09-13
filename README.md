# agy-guard

> **Deterministic AI Agent Governance, AST Blast-Radius Scanner & Verification Harness**

`agy-guard` is an autonomous enterprise governance tool designed to maintain strict integrity invariants across AI coding agents (Antigravity CLI `agy`, Claude Code, Cursor, Codex, OpenCode).

## Features

- **AST Blast-Radius Inspection**: Recursively pre-scan symbols and references across multi-language codebases before mutations (`agy-guard inspect-symbol <symbol>`).
- **Milestone-Gated Verification**: Run empirical compiler, linter, and test harness gates (`agy-guard verify`).
- **RAG & Memory Synchronization**: Automated checkpointing to Obsidian 4-file governance structure (`agy-guard checkpoint`).
- **Sanitized Env Inspection**: Safe audit of environment variables without credential exfiltration (`agy-guard inspect-env`).
- **Sovereign Git Push Guard**: Pre-push validation preventing unauthorized remote repository mutations (`agy-guard push`).

## Installation

### Option 1: Official PyPI
```bash
pip install agy-guard
```

### Option 2: Arch Linux (AUR)
```bash
yay -S agy-guard
```

### Option 3: macOS & Linux (Homebrew)
```bash
brew install zyekhabdul/tap/agy-guard
```

### Option 4: Android Termux
```bash
curl -fsSL https://raw.githubusercontent.com/zyekhabdul/termux-tap/main/setup.sh | bash
pkg install agy-guard
```

### Option 5: 1-Line Standalone Installer
```bash
curl -fsSL https://raw.githubusercontent.com/zyekhabdul/agy-guard/main/install.sh | bash
```

## Usage

```bash
# Verify environment and test suite
agy-guard verify

# Scan symbol blast radius
agy-guard inspect-symbol parse_token

# Check RAG status and sync rules
agy-guard sync-rules
agy-guard status
```

## License

MIT License (c) 2026 Zyekh Abdul
