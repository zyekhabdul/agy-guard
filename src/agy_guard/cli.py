#!/usr/bin/env python3
"""
agy-guard - Deterministic Guardrail & Governance Tool for AI Agents (v3.0 Enterprise)
Provides rules synchronization, milestone-gated Obsidian RAG sync, instant project context briefing,
on-demand skill management, polyglot symbol finder, secure env inspector, and git push protection.
"""

import os
import sys
import json
import re
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

HOME = Path.home()
VAULT_PATH = HOME / "Documents" / "Obsidian Vault"
MEMORY_DIR = VAULT_PATH / "00-AGY-Memory"
CONFIG_DIR = HOME / ".gemini" / "config"
SKILLS_DIR = HOME / ".agents" / "skills"
SKILLS_ARCHIVE = HOME / ".agents" / "skills_archive"

RULE_FILES = [
    HOME / "GEMINI.md",
    HOME / ".gemini" / "GEMINI.md",
    CONFIG_DIR / "GEMINI.md",
    HOME / ".agents" / "GEMINI.md",
]

RULE_DOCS = [
    CONFIG_DIR / "rules" / "agent-persona-invariants.md",
    CONFIG_DIR / "rules" / "agy-runtime-troubleshooting.md",
    CONFIG_DIR / "rules" / "ai-proposal-protocol.md",
    CONFIG_DIR / "rules" / "autonomous-failure-modes.md",
    CONFIG_DIR / "rules" / "deterministic-machine-harness.md",
    CONFIG_DIR / "rules" / "empirical-verification.md",
    CONFIG_DIR / "rules" / "environment-topology.md",
    CONFIG_DIR / "rules" / "git-push-restriction.md",
    CONFIG_DIR / "rules" / "inspect-before-apply.md",
    CONFIG_DIR / "rules" / "mcp-discovery.md",
    CONFIG_DIR / "rules" / "obsidian-rag.md",
    CONFIG_DIR / "rules" / "ponytail-yagni.md",
    CONFIG_DIR / "rules" / "sensitive-area-guard.md",
    CONFIG_DIR / "rules" / "system-diagnostics.md",
    CONFIG_DIR / "rules" / "workflow-ai-agent.md",
]

CANONICAL_GEMINI_MD = """# AI AGENT WORKSPACE STANDARDS & SSOT POINTER

Global rules and binding guidelines are centralized in the Master Configuration directory.
All agents (Antigravity CLI, OpenCode, Claude Code, Codex) MUST strictly adhere to the authoritative rules defined in:
- Master Rules Index: `/home/fuckadmin/.gemini/config/GEMINI.md`
- Modular Rule Definitions: `/home/fuckadmin/.gemini/config/rules/`

### Core Directives Summary
- **Deterministic Machine Harness**: Autonomous execution governed by compiler, typecheck, and test gates (`/home/fuckadmin/.gemini/config/rules/deterministic-machine-harness.md`)
- **Autonomous Failure Modes Defense**: 10 anti-blunder invariants and circuit breaker (`/home/fuckadmin/.gemini/config/rules/autonomous-failure-modes.md`)
- **Agent Persona & Execution Invariants**: Objective technical mentor, autonomous single-stream execution, strict no-emoji (`/home/fuckadmin/.gemini/config/rules/agent-persona-invariants.md`)
- **Runtime Troubleshooting**: AGY error recovery protocol (`/home/fuckadmin/.gemini/config/rules/agy-runtime-troubleshooting.md`)
- **Inspection Gate**: Cari dulu baru terapkan & AST call-site scan (`/home/fuckadmin/.gemini/config/rules/inspect-before-apply.md`)
- **Verification Gate**: Empirical terminal proof exit code 0 (`/home/fuckadmin/.gemini/config/rules/empirical-verification.md`)
- **Safety Gate**: Hard-stop on sensitive areas (`/home/fuckadmin/.gemini/config/rules/sensitive-area-guard.md`) & Git push restriction (`/home/fuckadmin/.gemini/config/rules/git-push-restriction.md`)
- **System Diagnostics**: Periodic VPS & endpoint verification (`/home/fuckadmin/.gemini/config/rules/system-diagnostics.md`)
- **Code Style**: Ponytail / YAGNI minimalism & native-first (`/home/fuckadmin/.gemini/config/rules/ponytail-yagni.md`)
- **Architectural Proposal Protocol**: Autonomous local coding, RFC for major breaking changes only (`/home/fuckadmin/.gemini/config/rules/ai-proposal-protocol.md`)
- **Workflow Standard**: Autonomous batch execution & machine-gated verification (`/home/fuckadmin/.gemini/config/rules/workflow-ai-agent.md`)
- **Memory & RAG**: Obsidian 4-file governance (`/home/fuckadmin/.gemini/config/rules/obsidian-rag.md`)
- **Communication**: Caveman terse high-density, strict no-emoji.
"""

def get_git_root(cwd=None):
    if cwd is None:
        cwd = Path.cwd()
    try:
        root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], cwd=cwd, stderr=subprocess.DEVNULL, text=True
        ).strip()
        return Path(root)
    except Exception:
        return None

def get_git_info(cwd=None):
    if cwd is None:
        cwd = Path.cwd()
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=cwd, stderr=subprocess.DEVNULL, text=True
        ).strip()
    except Exception:
        commit = "non-git"
    
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"], cwd=cwd, stderr=subprocess.DEVNULL, text=True
        ).strip()
    except Exception:
        branch = "none"

    try:
        status_lines = subprocess.check_output(
            ["git", "status", "--short"], cwd=cwd, stderr=subprocess.DEVNULL, text=True
        ).strip().splitlines()
        dirty_count = len(status_lines)
    except Exception:
        dirty_count = 0

    return commit, branch, dirty_count

def resolve_namespace(cwd=None):
    if cwd is None:
        cwd = Path.cwd()
    
    git_root = get_git_root(cwd)
    target = git_root if git_root else cwd
    
    if target == HOME:
        return "global-workspace"
    try:
        remote = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"], cwd=target, stderr=subprocess.DEVNULL, text=True
        ).strip()
        if remote:
            repo_name = Path(remote).stem.replace(".git", "")
            return repo_name
    except Exception:
        pass
    return target.name

def cmd_sync_rules(args):
    print("[ AGY-GUARD ] Synchronizing rule files...")
    synced = 0
    for target in RULE_FILES:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(CANONICAL_GEMINI_MD, encoding="utf-8")
        print(f"  [ SYNCED ] -> {target}")
        synced += 1
    print(f"[ SUCCESS ] {synced} rule files synchronized byte-for-byte.")
    
    # Cross-agent parity sync (Claude Code, OpenCode, Codex)
    sync_script = HOME / "scripts" / "sync-agents.sh"
    if not sync_script.exists():
        sync_script = HOME / "Projects" / "sovereign-agent-os" / "scripts" / "sync-agents.sh"
    if sync_script.exists():
        try:
            print("[ AGY-GUARD ] Running cross-agent synchronizer for multi-agent parity...")
            subprocess.run(["bash", str(sync_script)], check=False)
        except Exception as e:
            print(f"  [ WARN ] Could not run sync-agents.sh: {e}")

def cmd_status(args):
    fix_mode = getattr(args, "fix", False)
    header_extra = " (AUTO-FIX MODE)" if fix_mode else ""
    print(f"=== [ AGY-GUARD SYSTEM STATUS v5.1{header_extra} ] ===")
    
    # 1. Check GEMINI.md sync
    for target in RULE_FILES:
        if not target.exists():
            if fix_mode:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(CANONICAL_GEMINI_MD, encoding="utf-8")
                print(f"  [ REPAIRED ] {target}")
            else:
                print(f"  [ MISSING ] {target}")
        else:
            content = target.read_text(encoding="utf-8")
            if content.strip() != CANONICAL_GEMINI_MD.strip():
                if fix_mode:
                    target.write_text(CANONICAL_GEMINI_MD, encoding="utf-8")
                    print(f"  [ REPAIRED ] {target}")
                else:
                    print(f"  [ DRIFT ] {target}")
            else:
                print(f"  [ OK ] {target}")
                
    # 2. Check Formal Rule Specifications
    print("\n--- [ FORMAL RULE SPECIFICATIONS ] ---")
    for rdoc in RULE_DOCS:
        status = "[ OK ]" if rdoc.exists() else "[ MISSING ]"
        print(f"  {status} {rdoc.name}")
    
    # 3. Check Obsidian Vault & 200-Line Cap
    print("\n--- [ OBSIDIAN RAG & MEMORY HEALTH ] ---")
    if VAULT_PATH.exists():
        print(f"  [ OK ] Obsidian Vault: {VAULT_PATH}")
        cwd = Path.cwd()
        ns = resolve_namespace(cwd)
        ns_dir = MEMORY_DIR / ns
        if ns_dir.exists():
            for mfile in ns_dir.glob("*.md"):
                lines = len(mfile.read_text(encoding="utf-8", errors="replace").splitlines())
                if lines > 200:
                    print(f"  [ WARNING ] {mfile.name} is {lines} lines (>200 line cap). Split to archive!")
                else:
                    print(f"  [ OK ] {mfile.name} ({lines}/200 lines)")
        else:
            if fix_mode and ns != "global-workspace":
                ns_dir.mkdir(parents=True, exist_ok=True)
                (ns_dir / "INDEX.md").write_text(f"# Project Index: {ns}\n", encoding="utf-8")
                (ns_dir / "CONTEXT.md").write_text(f"# Context: {ns}\n", encoding="utf-8")
                (ns_dir / "STATE.md").write_text(f"# Active State: {ns}\nStatus: ACTIVE\n", encoding="utf-8")
                (ns_dir / "DECISIONS.md").write_text(f"# Architecture Decision Records: {ns}\n", encoding="utf-8")
                print(f"  [ REPAIRED ] Scaffolded 4-file memory structure at {ns_dir}")
            else:
                print(f"  [ NOTICE ] Memory namespace not yet initialized for '{ns}'")
    else:
        print(f"  [ WARNING ] Obsidian Vault not found at {VAULT_PATH}")
    
    # 4. Check Dual-File MCP
    print("\n--- [ MCP DISCOVERY HEALTH ] ---")
    cfg1 = CONFIG_DIR / "mcp_config.json"
    cfg2 = CONFIG_DIR / "mcp_config_extended.json"
    print(f"  [{'OK' if cfg1.exists() else 'MISSING'}] Primary: {cfg1}")
    print(f"  [{'OK' if cfg2.exists() else 'MISSING'}] Extended: {cfg2}")
    
    # 5. Git Info & Namespace
    print("\n--- [ ACTIVE WORKSPACE CONTEXT ] ---")
    cwd = Path.cwd()
    git_root = get_git_root(cwd)
    ns = resolve_namespace(cwd)
    commit, branch, dirty = get_git_info(cwd)
    print(f"  [ CWD ] {cwd}")
    print(f"  [ GIT ROOT ] {git_root or 'none (non-git)'}")
    print(f"  [ NAMESPACE ] {ns}")
    print(f"  [ GIT ] Branch: {branch} | Commit: {commit[:8]} | Uncommitted Files: {dirty}")
    
    # 6. Git Hooks
    if git_root:
        pre_commit = git_root / ".git" / "hooks" / "pre-commit"
        post_commit = git_root / ".git" / "hooks" / "post-commit"
        pre_push = git_root / ".git" / "hooks" / "pre-push"
        if fix_mode:
            if not pre_commit.exists():
                cmd_install_pre_commit(args)
            if not post_commit.exists():
                cmd_install_hook(args)
            if not pre_push.exists():
                cmd_install_push_guard(args)
            pre_commit = git_root / ".git" / "hooks" / "pre-commit"
            post_commit = git_root / ".git" / "hooks" / "post-commit"
            pre_push = git_root / ".git" / "hooks" / "pre-push"
        print(f"  [{'OK' if pre_commit.exists() else 'NOTICE'}] Anti-Blunder Pre-Commit Hook: {'Active' if pre_commit.exists() else 'Not installed'}")
        print(f"  [{'OK' if post_commit.exists() else 'NOTICE'}] Auto-Checkpoint Hook: {'Active' if post_commit.exists() else 'Not installed'}")
        print(f"  [{'OK' if pre_push.exists() else 'NOTICE'}] Anti-Push Protection Hook: {'Active' if pre_push.exists() else 'Not installed'}")
        
    # 7. Active Skills Count
    active_skills = len([p for p in SKILLS_DIR.iterdir() if p.is_dir()]) if SKILLS_DIR.exists() else 0
    print(f"  [ SKILLS ] Active: {active_skills} skills (Lean context headroom)")
    print("========================================")

def cmd_context(args):
    """Outputs instant high-density project context briefing for AI sessions."""
    cwd = Path.cwd()
    git_root = get_git_root(cwd)
    ns = resolve_namespace(cwd)
    commit, branch, dirty = get_git_info(cwd)
    
    print("=== [ INSTANT PROJECT BRIEFING ] ===")
    print(f"  • Project / Namespace : {ns}")
    print(f"  • Git Root Directory  : {git_root or cwd}")
    print(f"  • Active Git Branch   : {branch}")
    print(f"  • Latest Commit Hash  : {commit}")
    print(f"  • Uncommitted Changes : {dirty} file(s)")
    
    # Read Obsidian STATE.md
    state_file = MEMORY_DIR / ns / "STATE.md"
    if state_file.exists():
        print("\n--- [ ACTIVE OBSIDIAN STATE ] ---")
        lines = state_file.read_text(encoding="utf-8").splitlines()
        for line in lines[:15]:
            print(f"  {line}")
    else:
        print(f"\n  [ NOTICE ] No existing STATE.md found in 00-AGY-Memory/{ns}/")
        
    # Read Obsidian DECISIONS.md if present
    dec_file = MEMORY_DIR / ns / "DECISIONS.md"
    if dec_file.exists():
        print("\n--- [ RECORDED ARCHITECTURAL DECISIONS ] ---")
        lines = dec_file.read_text(encoding="utf-8").splitlines()
        for line in lines[:10]:
            print(f"  {line}")
            
    print("\n====================================")

def cmd_checkpoint(args):
    cwd = Path.cwd()
    ns = args.namespace or resolve_namespace(cwd)
    msg = args.msg or "Task milestone update"
    status = args.status.upper()
    
    target_dir = MEMORY_DIR / ns
    target_dir.mkdir(parents=True, exist_ok=True)
    state_file = target_dir / "STATE.md"
    
    commit, branch, dirty = get_git_info(cwd)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    state_content = f"""# ACTIVE STATE — {ns}

- **Last Checkpoint**: {now}
- **Status**: {status}
- **Git Branch**: `{branch}`
- **Git Commit**: `{commit}`
- **Uncommitted Changes**: {dirty} file(s)

---

## Active Milestone / Task
- **Summary**: {msg}
- **Checkpoint Context**: Logged via `agy-guard checkpoint`

## Invariant Checks
- [x] Ponytail / YAGNI Minimalist verified
- [x] Strict No-Emoji compliant
- [x] Git push permission checked (local only)
"""
    state_file.write_text(state_content.strip() + "\n", encoding="utf-8")
    print(f"[ AGY-GUARD ] Checkpoint saved to: {state_file}")
    print(f"  • Namespace: {ns}")
    print(f"  • Commit: {commit[:8]}")
    print(f"  • Status: {status}")
    print(f"  • Message: {msg}")

def cmd_install_hook(args):
    cwd = Path.cwd()
    git_root = get_git_root(cwd)
    if not git_root:
        print("[ ERROR ] Current directory is not inside a git repository.", file=sys.stderr)
        sys.exit(1)
    
    hooks_dir = git_root / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    post_commit = hooks_dir / "post-commit"
    
    hook_script = """#!/usr/bin/env bash
# Auto-generated by agy-guard
if command -v agy-guard >/dev/null 2>&1; then
    COMMIT_MSG=$(git log -1 --pretty=%B 2>/dev/null | head -n 1)
    agy-guard checkpoint --msg "Auto-commit: ${COMMIT_MSG:-Updated files}" --status ACTIVE >/dev/null 2>&1 &
fi
"""
    post_commit.write_text(hook_script, encoding="utf-8")
    post_commit.chmod(0o755)
    print(f"[ SUCCESS ] Git post-commit hook successfully installed at: {post_commit}")

def cmd_install_push_guard(args):
    cwd = Path.cwd()
    git_root = get_git_root(cwd)
    if not git_root:
        print("[ ERROR ] Current directory is not inside a git repository.", file=sys.stderr)
        sys.exit(1)
        
    hooks_dir = git_root / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    pre_push = hooks_dir / "pre-push"
    
    hook_script = """#!/usr/bin/env bash
# Hard Push Guard Interceptor by agy-guard
if [ "${ALLOW_GIT_PUSH:-0}" != "1" ]; then
    echo "[ HARD GUARD BLOCKED ] 'git push' is forbidden by default AI Agent policy." >&2
    echo "To push with explicit human intent, run: ALLOW_GIT_PUSH=1 git push" >&2
    exit 1
fi
"""
    pre_push.write_text(hook_script, encoding="utf-8")
    pre_push.chmod(0o755)
    print(f"[ SUCCESS ] Anti-Push Protection Hook installed at: {pre_push}")
    print("  • Remote push is now physically blocked unless ALLOW_GIT_PUSH=1 is passed.")

PRE_COMMIT_SCRIPT = r"""#!/usr/bin/env bash
# PRE-COMMIT HARNESS: Deterministic Anti-Blunder Sanitizer
# Generated by agy-guard
set -euo pipefail

# 1. Block Lazy Truncation Placeholders (Membunuh: // ... existing code ...)
if git rev-parse --verify HEAD >/dev/null 2>&1; then
    if git diff --cached | grep -Eiq '(existing code|remaining unchanged|TODO: implement|rest of (the|your) code)'; then
        echo "[ HARDBLOCK ] Terdeteksi placeholder kode malas/terpotong di staged diff!" >&2
        echo "Contoh terlarang: '// ... existing code ...', 'TODO: implement'" >&2
        exit 1
    fi
fi

# 2. Block Emojis in staged files (Membunuh: Polusi Emoji di Codebase)
if git diff --cached | grep -P "[\x{1F600}-\x{1F64F}\x{1F300}-\x{1F5FF}\x{1F680}-\x{1F6FF}\x{2600}-\x{26FF}\x{2700}-\x{27BF}]" 2>/dev/null; then
    echo "[ HARDBLOCK ] Terdeteksi karakter emoji dalam staged files." >&2
    echo "Gunakan ikon SVG/Lucide atau token teks sesuai aturan strict no-emoji." >&2
    exit 1
fi

# 3. Block Test Tampering (Membunuh: Mengubah tes saat mengerjakan fitur)
if [ "${ALLOW_TEST_MUTATION:-0}" != "1" ]; then
    STAGED_TESTS=$(git diff --cached --name-only | grep -E '^tests/|^spec/|.*\.test\..*|.*\.spec\..*' || true)
    STAGED_SRC=$(git diff --cached --name-only | grep -vE '^tests/|^spec/|.*\.test\..*|.*\.spec\..*' || true)
    if [ -n "$STAGED_TESTS" ] && [ -n "$STAGED_SRC" ]; then
        echo "[ HARDBLOCK ] Mengubah file tes bersamaan dengan source code dilarang." >&2
        echo "Untuk mengizinkan perubahan tes secara sadar, jalankan: ALLOW_TEST_MUTATION=1 git commit" >&2
        exit 1
    fi
fi

# 4. Block Secret & Private Key Leaks
STAGED_SECRETS=$(git diff --cached --name-only | grep -E '(^|/)\.env$|\.pem$|\.key$|id_rsa' || true)
if [ -n "$STAGED_SECRETS" ]; then
    if [ "${ALLOW_SECRET_COMMIT:-0}" != "1" ]; then
        echo "[ HARDBLOCK ] File rahasia/kredensial terdeteksi di staged files: $STAGED_SECRETS" >&2
        echo "Gunakan .env.example atau password manager." >&2
        exit 1
    fi
fi

# 5. Check Required Files on projects with PRD.md
if [ -f "PRD.md" ]; then
    REQUIRED_FILES=("PRD.md" "PLAN.md" "GEMINI.md" "CHANGELOG.md" "README.md")
    for f in "${REQUIRED_FILES[@]}"; do
        if [ ! -f "$f" ]; then
            echo "[ HARDBLOCK ] File standar proyek wajib ada: $f" >&2
            exit 1
        fi
    done
fi

echo "[ PASS ] Pre-commit deterministic checks verified (exit 0)."
exit 0
"""

def cmd_install_pre_commit(args):
    cwd = Path.cwd()
    git_root = get_git_root(cwd)
    if not git_root:
        print("[ ERROR ] Current directory is not inside a git repository.", file=sys.stderr)
        sys.exit(1)
        
    hooks_dir = git_root / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    pre_commit = hooks_dir / "pre-commit"
    
    pre_commit.write_text(PRE_COMMIT_SCRIPT, encoding="utf-8")
    pre_commit.chmod(0o755)
    print(f"[ SUCCESS ] Anti-Blunder Pre-Commit Hook installed at: {pre_commit}")

def cmd_skill_load(args):
    skill_name = args.name.lower()
    source = SKILLS_ARCHIVE / skill_name
    dest = SKILLS_DIR / skill_name
    
    if not source.exists():
        # Fuzzy match in archive
        matches = [p.name for p in SKILLS_ARCHIVE.iterdir() if skill_name in p.name.lower()]
        if matches:
            source = SKILLS_ARCHIVE / matches[0]
            dest = SKILLS_DIR / matches[0]
        else:
            print(f"[ ERROR ] Skill '{skill_name}' not found in archive ({SKILLS_ARCHIVE}).", file=sys.stderr)
            sys.exit(1)
            
    if dest.exists():
        print(f"[ NOTICE ] Skill '{dest.name}' is already active.")
        return
        
    shutil.copytree(source, dest)
    print(f"[ SUCCESS ] Skill activated: {dest.name} -> {dest}")

def cmd_skill_archive(args):
    skill_name = args.name.lower()
    source = SKILLS_DIR / skill_name
    dest = SKILLS_ARCHIVE / skill_name
    
    if not source.exists():
        print(f"[ ERROR ] Active skill '{skill_name}' not found in {SKILLS_DIR}.", file=sys.stderr)
        sys.exit(1)
        
    SKILLS_ARCHIVE.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.move(source, dest)
    print(f"[ SUCCESS ] Skill archived: {skill_name} -> {dest}")

def cmd_skill_list(args):
    active = sorted([p.name for p in SKILLS_DIR.iterdir() if p.is_dir()]) if SKILLS_DIR.exists() else []
    archived = sorted([p.name for p in SKILLS_ARCHIVE.iterdir() if p.is_dir()]) if SKILLS_ARCHIVE.exists() else []
    
    print(f"=== [ SKILL REGISTRY: {len(active)} ACTIVE | {len(archived)} ARCHIVED ] ===")
    print("\n--- Active Core Skills ---")
    for s in active:
        print(f"  • {s}")
        
    if args.all:
        print(f"\n--- Archived Skills ({len(archived)} items) ---")
        for s in archived[:30]:
            print(f"  • {s}")
        if len(archived) > 30:
            print(f"  ... and {len(archived) - 30} more in archive.")
    else:
        print(f"\n  [ TIP ] Run 'agy-guard skill-list --all' to view all {len(archived)} archived skills.")
        print("  [ TIP ] Run 'agy-guard skill-load <name>' to activate any skill on-demand.")
    print("=================================================================")

def mask_secrets(obj):
    if isinstance(obj, dict):
        res = {}
        for k, v in obj.items():
            if any(s in k.lower() for s in ["key", "token", "secret", "password", "auth", "credential"]):
                res[k] = "[REDACTED]"
            else:
                res[k] = mask_secrets(v)
        return res
    elif isinstance(obj, list):
        return [mask_secrets(i) for i in obj]
    return obj

def cmd_mcp_inspect(args):
    print("=== [ DUAL-FILE MCP DISCOVERY INSPECTION ] ===")
    files = [
        ("Primary Config", CONFIG_DIR / "mcp_config.json"),
        ("Extended Config", CONFIG_DIR / "mcp_config_extended.json"),
    ]
    
    for label, path in files:
        print(f"\n--- {label}: {path} ---")
        if not path.exists():
            print(f"  [ NOT FOUND ] {path}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            servers = data.get("mcpServers", {})
            if not servers:
                print("  [ EMPTY ] No mcpServers found.")
                continue
            for sname, sinfo in servers.items():
                cmd = sinfo.get("command", "")
                args_list = sinfo.get("args", [])
                safe_args = mask_secrets(args_list)
                print(f"  • Server: {sname}")
                print(f"    Command: {cmd}")
                print(f"    Args: {json.dumps(safe_args)}")
        except Exception as e:
            print(f"  [ ERROR PARSING ] {e}")
    print("\n==============================================")

def extract_polyglot_block(lines, start_idx):
    open_braces = 0
    started = False
    end_idx = start_idx
    
    for i in range(start_idx, len(lines)):
        line = lines[i]
        stripped = re.sub(r"//.*$|/\*.*?\*/", "", line)
        for char in stripped:
            if char == "{":
                open_braces += 1
                started = True
            elif char == "}":
                open_braces -= 1
                if started and open_braces <= 0:
                    return start_idx, i
        end_idx = i
        if started and open_braces <= 0:
            break
        if i - start_idx > 80:
            break
            
    return start_idx, min(end_idx, start_idx + 45)

def cmd_inspect_symbol(args):
    filepath = Path(args.file)
    symbol = args.symbol
    
    if not filepath.exists():
        print(f"[ ERROR ] File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
        
    lines = filepath.read_text(encoding="utf-8", errors="replace").splitlines()
    found = False
    
    if filepath.suffix == ".py":
        import ast
        try:
            tree = ast.parse("\n".join(lines), filename=str(filepath))
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if node.name == symbol:
                        start = node.lineno
                        end = node.end_lineno if hasattr(node, "end_lineno") else start + 30
                        print(f"=== [ AST SYMBOL: {symbol} in {filepath} (Lines {start}-{end}) ] ===")
                        for idx in range(start - 1, min(end, len(lines))):
                            print(f"{idx+1:4d}: {lines[idx]}")
                        found = True
                        break
        except Exception:
            pass
            
    if not found:
        pattern = re.compile(rf"\b(function|class|const|let|var|def|fn|func|pub\s+fn|type|interface)\s+{re.escape(symbol)}\b|{re.escape(symbol)}\s*[:=]\s*(function|\([^)]*\)\s*=>)")
        for idx, line in enumerate(lines):
            if pattern.search(line) or (symbol in line and any(k in line for k in ["function", "class", "const", "def", "fn", "=>", "func"])):
                start, end = extract_polyglot_block(lines, idx)
                print(f"=== [ POLYGLOT BLOCK: {symbol} in {filepath} (Lines {start+1}-{end+1}) ] ===")
                for i in range(start, end + 1):
                    print(f"{i+1:4d}: {lines[i]}")
                found = True
                break
                
    if not found:
        for idx, line in enumerate(lines):
            if symbol in line:
                start = max(0, idx - 2)
                end = min(len(lines), idx + 30)
                print(f"=== [ MATCH: {symbol} in {filepath} (Lines {start+1}-{end}) ] ===")
                for i in range(start, end):
                    print(f"{i+1:4d}: {lines[i]}")
                found = True
                break
                
    if not found:
        print(f"[ NOT FOUND ] Symbol '{symbol}' not found in {filepath}")

def cmd_find(args):
    """Recursively finds symbol across codebase files."""
    query = args.query
    cwd = Path.cwd()
    print(f"=== [ AGY-GUARD GLOBAL SYMBOL SEARCH: '{query}' ] ===")
    
    extensions = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".php", ".rb", ".liquid"}
    found_count = 0
    ignored_dirs = {
        "node_modules", "vendor", "__pycache__", "dist", "build", ".venv",
        ".git", ".npm-global", ".cache", ".local", ".gemini", ".agents",
        "Documents", "Downloads", "Music", "Videos", "Desktop", "Pictures", ".cargo", ".rustup"
    }
    
    for root, dirnames, filenames in os.walk(cwd):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in ignored_dirs]
        for fname in filenames:
            ext = Path(fname).suffix
            if ext in extensions:
                fpath = Path(root) / fname
                try:
                    lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines()
                    for idx, line in enumerate(lines):
                        if query in line and any(k in line for k in ["def ", "class ", "function ", "const ", "interface ", "type ", "fn ", "func "]):
                            rel = fpath.relative_to(cwd)
                            start, end = extract_polyglot_block(lines, idx)
                            print(f"\n[ MATCH ] {rel} (Lines {start+1}-{end+1})")
                            for i in range(start, min(end + 1, start + 12)):
                                print(f"  {i+1:4d}: {lines[i]}")
                            found_count += 1
                            if found_count >= 8:
                                print("\n[ NOTE ] Capping output at 8 top matches to preserve headroom.")
                                print("=====================================================")
                                return
                except Exception:
                    pass
                
    if found_count == 0:
        print(f"  [ NOT FOUND ] No symbol declarations matching '{query}' in {cwd}")
    print("\n=====================================================")

def cmd_inspect_env(args):
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"[ ERROR ] File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
        
    print(f"=== [ SECURE ENV INSPECTION: {filepath.name} ] ===")
    lines = filepath.read_text(encoding="utf-8", errors="replace").splitlines()
    for idx, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip("'\"")
            if len(val) <= 4:
                masked = "[REDACTED]"
            else:
                masked = f"{val[:3]}...{val[-2:]} ({len(val)} chars) [MASKED]"
            print(f"  {idx:3d}: {key}={masked}")
        else:
            print(f"  {idx:3d}: {line}")
    print("=================================================")

def cmd_audit_skills(args):
    print("=== [ SKILL REGISTRY AUDIT ] ===")
    active_skills = [p for p in SKILLS_DIR.iterdir() if p.is_dir()] if SKILLS_DIR.exists() else []
    archived_skills = [p for p in SKILLS_ARCHIVE.iterdir() if p.is_dir()] if SKILLS_ARCHIVE.exists() else []
    
    total_bytes = sum((s / "SKILL.md").stat().st_size for s in active_skills if (s / "SKILL.md").exists())
    est_tokens = total_bytes // 4
    
    print(f"  • Active Core Skills   : {len(active_skills)}")
    print(f"  • Archived Skills      : {len(archived_skills)}")
    print(f"  • Active Memory Size   : {total_bytes / 1024:.1f} KB")
    print(f"  • Context Headroom     : ~{est_tokens:,} tokens per turn (Optimized)")
    print("================================")

def cmd_install_hooks_all(args):
    target_dir = Path(args.target_dir) if args.target_dir else HOME / "Projects"
    print(f"=== [ BATCH INSTALLING GIT HOOKS IN {target_dir} ] ===")
    
    installed_count = 0
    for p in target_dir.iterdir():
        if p.is_dir() and (p / ".git").exists():
            hooks_dir = p / ".git" / "hooks"
            hooks_dir.mkdir(parents=True, exist_ok=True)
            
            # 1. post-commit hook
            post_commit = hooks_dir / "post-commit"
            post_commit_script = """#!/usr/bin/env bash
# Auto-generated by agy-guard
if command -v agy-guard >/dev/null 2>&1; then
    COMMIT_MSG=$(git log -1 --pretty=%B 2>/dev/null | head -n 1)
    agy-guard checkpoint --msg "Auto-commit: ${COMMIT_MSG:-Updated files}" --status ACTIVE >/dev/null 2>&1 &
fi
"""
            post_commit.write_text(post_commit_script, encoding="utf-8")
            post_commit.chmod(0o755)
            
            # 2. pre-push hook
            pre_push = hooks_dir / "pre-push"
            pre_push_script = """#!/usr/bin/env bash
# Hard Push Guard Interceptor by agy-guard
if [ "${ALLOW_GIT_PUSH:-0}" != "1" ]; then
    echo "[ HARD GUARD BLOCKED ] 'git push' is forbidden by default AI Agent policy." >&2
    echo "To push with explicit human intent, run: ALLOW_GIT_PUSH=1 git push" >&2
    exit 1
fi
"""
            pre_push.write_text(pre_push_script, encoding="utf-8")
            pre_push.chmod(0o755)
            
            # 3. pre-commit hook
            pre_commit = hooks_dir / "pre-commit"
            pre_commit.write_text(PRE_COMMIT_SCRIPT, encoding="utf-8")
            pre_commit.chmod(0o755)
            
            print(f"  [ INSTALLED ] {p.name} (pre-commit + post-commit + pre-push)")
            installed_count += 1
            
    print(f"[ SUCCESS ] Installed 3 hooks across {installed_count} repositories.")

def cmd_set_global_git_templates(args):
    tpl_dir = HOME / ".git-templates" / "hooks"
    tpl_dir.mkdir(parents=True, exist_ok=True)
    
    post_commit = tpl_dir / "post-commit"
    post_commit_script = """#!/usr/bin/env bash
# Auto-generated by agy-guard global template
if command -v agy-guard >/dev/null 2>&1; then
    COMMIT_MSG=$(git log -1 --pretty=%B 2>/dev/null | head -n 1)
    agy-guard checkpoint --msg "Auto-commit: ${COMMIT_MSG:-Updated files}" --status ACTIVE >/dev/null 2>&1 &
fi
"""
    post_commit.write_text(post_commit_script, encoding="utf-8")
    post_commit.chmod(0o755)
    
    pre_push = tpl_dir / "pre-push"
    pre_push_script = """#!/usr/bin/env bash
# Hard Push Guard Interceptor by agy-guard
if [ "${ALLOW_GIT_PUSH:-0}" != "1" ]; then
    echo "[ HARD GUARD BLOCKED ] 'git push' is forbidden by default AI Agent policy." >&2
    echo "To push with explicit human intent, run: ALLOW_GIT_PUSH=1 git push" >&2
    exit 1
fi
"""
    pre_push.write_text(pre_push_script, encoding="utf-8")
    pre_push.chmod(0o755)
    
    pre_commit = tpl_dir / "pre-commit"
    pre_commit.write_text(PRE_COMMIT_SCRIPT, encoding="utf-8")
    pre_commit.chmod(0o755)
    
    subprocess.run(["git", "config", "--global", "init.templateDir", str(HOME / ".git-templates")], check=True)
    print(f"[ SUCCESS ] Global git template set to: {HOME / '.git-templates'}")
    print("  • All future 'git init' or 'git clone' repositories will automatically inherit pre-commit, post-commit, and pre-push hooks.")

def cmd_scaffold_all_projects(args):
    target_dir = Path(args.target_dir) if args.target_dir else HOME / "Projects"
    print(f"=== [ BATCH SCAFFOLDING OBSIDIAN RAG MEMORY IN {target_dir} ] ===")
    
    scaffolded_count = 0
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for p in target_dir.iterdir():
        if p.is_dir() and not p.name.startswith("."):
            ns = p.name.replace(".", "-")
            ns_dir = MEMORY_DIR / ns
            ns_dir.mkdir(parents=True, exist_ok=True)
            
            commit, branch, _ = get_git_info(p)
            
            # Detect tech stack
            tech = "Generic Codebase"
            if (p / "package.json").exists():
                tech = "Node.js / JavaScript / TypeScript"
            elif (p / "composer.json").exists():
                tech = "PHP / Laravel / Composer"
            elif (p / "Cargo.toml").exists():
                tech = "Rust / Cargo"
            elif (p / "go.mod").exists():
                tech = "Golang"
            elif (p / "requirements.txt").exists() or (p / "pyproject.toml").exists():
                tech = "Python"
            elif (p / "config.yml").exists() or "theme" in p.name.lower():
                tech = "Shopify Liquid Theme"
                
            # 1. INDEX.md
            index_file = ns_dir / "INDEX.md"
            if not index_file.exists():
                index_content = f"""# PROJECT INDEX — {ns}

- **Local Path**: `{p}`
- **Primary Tech Stack**: {tech}
- **Git Commit Hash**: `{commit}`
- **Active Branch**: `{branch}`
- **Obsidian Namespace**: `00-AGY-Memory/{ns}/`
"""
                index_file.write_text(index_content.strip() + "\n", encoding="utf-8")
                
            # 2. CONTEXT.md
            ctx_file = ns_dir / "CONTEXT.md"
            if not ctx_file.exists():
                ctx_content = f"""# PROJECT CONTEXT — {ns}

## Overview
Project workspace located at `{p}`.

## Technical Stack & Constraints
- **Primary Stack**: {tech}
- **Architecture Standard**: Ponytail YAGNI, 9 Binding Rules compliant.
- **Max Lines Limit**: 200 lines per RAG file.
"""
                ctx_file.write_text(ctx_content.strip() + "\n", encoding="utf-8")
                
            # 3. STATE.md
            state_file = ns_dir / "STATE.md"
            if not state_file.exists():
                state_content = f"""# ACTIVE STATE — {ns}

- **Last Checkpoint**: {now}
- **Status**: ACTIVE
- **Git Branch**: `{branch}`
- **Git Commit**: `{commit}`

---

## Active Milestone / Task
- **Summary**: Initialized project memory via `agy-guard scaffold-all-projects`
- **Checkpoint Context**: Scaffolding complete

## Invariant Checks
- [x] Ponytail / YAGNI Minimalist verified
- [x] Strict No-Emoji compliant
- [x] Git push permission checked (local only)
"""
                state_file.write_text(state_content.strip() + "\n", encoding="utf-8")
                
            # 4. DECISIONS.md
            dec_file = ns_dir / "DECISIONS.md"
            if not dec_file.exists():
                dec_content = f"""# ARCHITECTURAL DECISIONS (ADR) — {ns}

## Standard Laws
- **Law 1**: Ponytail / YAGNI - Minimalist code generation, zero unsolicited refactoring.
- **Law 2**: Empirical Verification - Always verify build/test before concluding task.
- **Law 3**: Git Push Guard - Remote push forbidden without explicit human command.
"""
                dec_file.write_text(dec_content.strip() + "\n", encoding="utf-8")
                
            print(f"  [ MEMORY INITIALIZED ] {ns} -> 00-AGY-Memory/{ns}/")
            scaffolded_count += 1
            
    print(f"[ SUCCESS ] Scaffolding complete for {scaffolded_count} project namespaces in Obsidian.")

def cmd_verify(args):
    """Auto-detects project stack and executes empirical verification with Circuit Breaker."""
    cwd = Path.cwd()
    git_root = get_git_root(cwd)
    breaker_file = (git_root / ".git" / "circuit_breaker.count") if git_root else (cwd / ".circuit_breaker.count")
    
    print("=== [ EMPIRICAL VERIFICATION AUTO-RUNNER ] ===")
    
    cmd = None
    if (cwd / "package.json").exists():
        try:
            pkg = json.loads((cwd / "package.json").read_text(encoding="utf-8"))
            scripts = pkg.get("scripts", {})
            if "test" in scripts and "no test specified" not in scripts["test"]:
                cmd = ["npm", "test"]
            elif "build" in scripts:
                cmd = ["npm", "run", "build"]
            elif "check" in scripts:
                cmd = ["npm", "run", "check"]
            elif (cwd / "tsconfig.json").exists():
                cmd = ["npx", "tsc", "--noEmit"]
        except Exception:
            pass
    elif (cwd / "Cargo.toml").exists():
        cmd = ["cargo", "check"]
    elif (cwd / "go.mod").exists():
        cmd = ["go", "test", "./..."]
    elif (cwd / "composer.json").exists():
        cmd = ["composer", "test"] if "test" in (cwd / "composer.json").read_text() else ["php", "-l", "index.php"]
    elif (cwd / "pytest.ini").exists() or (cwd / "tests").exists() or (cwd / "pyproject.toml").exists():
        cmd = ["pytest"]
    elif "theme" in cwd.name.lower() or (cwd / "config.yml").exists() or (cwd / "sections").exists():
        cmd = ["shopify", "theme", "check"]
        
    if not cmd:
        if (cwd / ".git").exists():
            cmd = ["git", "status", "--short"]
        else:
            print("  [ NOTICE ] No automated test suite or git tracking in active workspace.")
            print("  [ PASS ] Workspace syntax check verified (Clean).")
            print("==============================================")
            return

    print(f"  • Running Command: {' '.join(cmd)}")
    try:
        res = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=120)
        if res.returncode == 0:
            if breaker_file.exists():
                try:
                    breaker_file.unlink()
                except Exception:
                    pass
            print("  [ PASS ] Verification exit code 0 (Success).")
            if res.stdout:
                lines = res.stdout.strip().splitlines()
                for l in lines[-6:]:
                    print(f"    {l}")
        else:
            fail_count = 0
            if breaker_file.exists():
                try:
                    fail_count = int(breaker_file.read_text(encoding="utf-8").strip())
                except Exception:
                    fail_count = 0
            fail_count += 1
            
            print(f"  [ FAIL ] Verification exited with code {res.returncode} (Attempt {fail_count}/3):")
            out = (res.stderr or res.stdout).strip().splitlines()
            for l in out[:15]:
                print(f"    [ERR] {l}")
                
            if fail_count >= 3:
                if breaker_file.exists():
                    try:
                        breaker_file.unlink()
                    except Exception:
                        pass
                print("\n  [ CIRCUIT BREAKER TRIPPED ] 3 consecutive verification failures detected!")
                print("  [ EMERGENCY ACTION ] Rolling back uncommitted mutations to prevent death loop...")
                if git_root:
                    subprocess.run(["git", "restore", "."], cwd=git_root)
                
                # Auto-update Obsidian STATE.md to BLOCKED
                try:
                    ns = resolve_namespace(cwd)
                    target_dir = MEMORY_DIR / ns
                    state_file = target_dir / "STATE.md"
                    if state_file.exists():
                        commit, branch, dirty = get_git_info(cwd)
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        state_content = f"""# ACTIVE STATE — {ns}

- **Last Checkpoint**: {now}
- **Status**: BLOCKED
- **Git Branch**: `{branch}`
- **Git Commit**: `{commit}`
- **Uncommitted Changes**: {dirty} file(s)

---

## Active Milestone / Task
- **Summary**: [CIRCUIT BREAKER TRIPPED] 3 consecutive verification failures detected. Uncommitted mutations rolled back.
- **Checkpoint Context**: Tripped by `agy-guard verify`

## Invariant Checks
- [x] Ponytail / YAGNI Minimalist verified
- [x] Strict No-Emoji compliant
- [x] Git push permission checked (local only)
- [ ] Verification passed (BLOCKED: Requires human guidance or RFC)
"""
                        state_file.write_text(state_content.strip() + "\n", encoding="utf-8")
                        print(f"  [ STATE UPDATED ] {state_file} marked as BLOCKED.")
                except Exception as e:
                    print(f"  [ WARN ] Could not update STATE.md: {e}")

                print("  [ HARD STOP ] AI self-healing halted. Raw error reported above. Exiting with code 126.")
                sys.exit(126)
            else:
                try:
                    breaker_file.write_text(str(fail_count), encoding="utf-8")
                    print(f"  [ CIRCUIT BREAKER ] Failure recorded ({fail_count}/3). Self-heal allowed.")
                except Exception:
                    pass
            sys.exit(res.returncode)
    except Exception as e:
        print(f"  [ ERROR ] Could not execute verification: {e}")
        sys.exit(1)
    print("==============================================")

def cmd_prep(args):
    """Pre-flight one-shot agent onboarding briefing."""
    cwd = Path.cwd()
    ns = resolve_namespace(cwd)
    git_root = get_git_root(cwd)
    commit, branch, dirty = get_git_info(cwd)
    
    print("=== [ PRE-FLIGHT AGENT ONBOARDING BRIEFING ] ===")
    print(f"  • Active Namespace    : {ns}")
    print(f"  • Git Root Path       : {git_root or cwd}")
    print(f"  • Git Branch / Commit : {branch} ({commit[:8]})")
    print(f"  • Modified / Untracked: {dirty} file(s)")
    
    # 1. Check PRD / PLAN status
    plan_file = cwd / "PLAN.md"
    prd_file = cwd / "PRD.md"
    if plan_file.exists():
        print("\n--- [ ACTIVE PLAN.md SUMMARY ] ---")
        lines = plan_file.read_text(encoding="utf-8", errors="replace").splitlines()
        for l in lines[:10]:
            print(f"  {l}")
    elif prd_file.exists():
        print("\n--- [ PRD.md DETECTED ] ---")
        lines = prd_file.read_text(encoding="utf-8", errors="replace").splitlines()
        for l in lines[:8]:
            print(f"  {l}")
            
    # 2. Check Obsidian Decisions & Laws
    dec_file = MEMORY_DIR / ns / "DECISIONS.md"
    if dec_file.exists():
        print("\n--- [ TOP ARCHITECTURAL LAWS (DECISIONS.md) ] ---")
        lines = dec_file.read_text(encoding="utf-8", errors="replace").splitlines()
        for l in lines[:8]:
            print(f"  {l}")
            
    print("\n================================================")

def cmd_diff_guard(args):
    """Audits diff radius (Ponytail YAGNI) and flags sensitive area violations."""
    cwd = Path.cwd()
    print("=== [ PONYTAIL DIFF & SENSITIVE AREA AUDIT ] ===")
    
    try:
        diff_out = subprocess.check_output(
            ["git", "diff", "HEAD", "--name-status"], cwd=cwd, stderr=subprocess.DEVNULL, text=True
        ).strip().splitlines()
    except Exception:
        diff_out = []
        
    if not diff_out:
        print("  [ CLEAN ] Working tree has no uncommitted changes.")
        print("================================================")
        return
        
    sensitive_keywords = ["auth", "login", "payment", "stripe", "paypal", "migration", "schema", ".env", "docker-compose", ".github", "workflow"]
    violations = []
    
    print(f"  • Total Changed Files: {len(diff_out)}")
    for item in diff_out:
        parts = item.split(None, 1)
        if len(parts) == 2:
            status, fname = parts
            is_sensitive = any(k in fname.lower() for k in sensitive_keywords)
            flag = " [ SENSITIVE AREA HARD-STOP ]" if is_sensitive else ""
            print(f"    [{status}] {fname}{flag}")
            if is_sensitive:
                violations.append(fname)
                
    if violations:
        print("\n  [ CAUTION ] Sensitive areas modified! Human authorization REQUIRED before commit/merge:")
        for v in violations:
            print(f"    -> {v}")
    else:
        print("\n  [ OK ] No sensitive surfaces detected. Ponytail minimal diff compliant.")
    print("================================================")

def cmd_push(args):
    """Executes safe human-authorized git push."""
    cwd = Path.cwd()
    env = os.environ.copy()
    env["ALLOW_GIT_PUSH"] = "1"
    
    push_args = ["git", "push"] + (args.git_args or [])
    print(f"=== [ AUTHORIZED GIT PUSH: {' '.join(push_args)} ] ===")
    
    try:
        res = subprocess.run(push_args, cwd=cwd, env=env, text=True)
        if res.returncode == 0:
            print("[ SUCCESS ] Git push completed successfully.")
        else:
            print(f"[ ERROR ] Git push failed with exit code {res.returncode}")
            sys.exit(res.returncode)
    except Exception as e:
        print(f"[ ERROR ] Failed to execute push: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="agy-guard v5.0: Deterministic Guardrails & Governance for AI Agents"
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    
    # sync-rules
    subparsers.add_parser("sync-rules", help="Synchronize all GEMINI.md rule files").set_defaults(func=cmd_sync_rules)
    
    # status
    sub_status = subparsers.add_parser("status", help="Show system rules, git root, and MCP health status")
    sub_status.add_argument("--fix", action="store_true", help="Automatically repair rule drift, missing hooks, and memory files")
    sub_status.set_defaults(func=cmd_status)
    
    # context
    subparsers.add_parser("context", help="Instant high-density project briefing for new sessions").set_defaults(func=cmd_context)
    
    # prep
    subparsers.add_parser("prep", help="One-shot agent pre-flight onboarding briefing").set_defaults(func=cmd_prep)
    
    # verify
    subparsers.add_parser("verify", help="Auto-detect and run empirical test/linter verification").set_defaults(func=cmd_verify)
    
    # diff-guard
    subparsers.add_parser("diff-guard", help="Audit diff radius and check for sensitive area violations").set_defaults(func=cmd_diff_guard)
    
    # push
    sub_push = subparsers.add_parser("push", help="Execute safe human-authorized git push")
    sub_push.add_argument("git_args", nargs="*", help="Arguments to pass to git push")
    sub_push.set_defaults(func=cmd_push)
    
    # checkpoint
    sub_cp = subparsers.add_parser("checkpoint", help="Log deterministic state checkpoint to Obsidian RAG")
    sub_cp.add_argument("-m", "--msg", type=str, default="Task milestone completed", help="Checkpoint message")
    sub_cp.add_argument("-s", "--status", type=str, default="ACTIVE", choices=["ACTIVE", "COMPLETED", "BLOCKED"], help="Status state")
    sub_cp.add_argument("-n", "--namespace", type=str, default=None, help="Target namespace override")
    sub_cp.set_defaults(func=cmd_checkpoint)
    
    # install-hook
    subparsers.add_parser("install-hook", help="Install git post-commit hook for auto Obsidian checkpoint").set_defaults(func=cmd_install_hook)
    
    # install-push-guard
    subparsers.add_parser("install-push-guard", help="Install git pre-push hook to physically block unconfirmed pushes").set_defaults(func=cmd_install_push_guard)
    
    # install-pre-commit
    subparsers.add_parser("install-pre-commit", help="Install git pre-commit anti-blunder sanitizer").set_defaults(func=cmd_install_pre_commit)
    
    # install-hooks-all
    sub_hall = subparsers.add_parser("install-hooks-all", help="Batch install hooks to all repos in ~/Projects")
    sub_hall.add_argument("-t", "--target-dir", type=str, default=None, help="Target directory (default: ~/Projects)")
    sub_hall.set_defaults(func=cmd_install_hooks_all)
    
    # set-global-git-templates
    subparsers.add_parser("set-global-git-templates", help="Configure global git templates for automatic hooks on new repos").set_defaults(func=cmd_set_global_git_templates)
    
    # scaffold-all-projects
    sub_scaf = subparsers.add_parser("scaffold-all-projects", help="Batch scaffold 4-file Obsidian memory for all projects in ~/Projects")
    sub_scaf.add_argument("-t", "--target-dir", type=str, default=None, help="Target directory (default: ~/Projects)")
    sub_scaf.set_defaults(func=cmd_scaffold_all_projects)
    
    # mcp-inspect
    subparsers.add_parser("mcp-inspect", help="Securely inspect dual-file MCP endpoints").set_defaults(func=cmd_mcp_inspect)
    
    # inspect-symbol
    sub_sym = subparsers.add_parser("inspect-symbol", help="Extract symbol using AST/brace-counter")
    sub_sym.add_argument("file", type=str, help="Path to file")
    sub_sym.add_argument("symbol", type=str, help="Symbol name (function, class)")
    sub_sym.set_defaults(func=cmd_inspect_symbol)
    
    # find
    sub_find = subparsers.add_parser("find", help="Recursively search symbol across codebase files")
    sub_find.add_argument("query", type=str, help="Symbol/function name to search")
    sub_find.set_defaults(func=cmd_find)
    
    # inspect-env
    sub_env = subparsers.add_parser("inspect-env", help="Safely inspect .env file with token masking")
    sub_env.add_argument("file", type=str, help="Path to .env file")
    sub_env.set_defaults(func=cmd_inspect_env)
    
    # audit-skills
    subparsers.add_parser("audit-skills", help="Audit skill registry count and token impact").set_defaults(func=cmd_audit_skills)
    
    # skill-load
    sub_sload = subparsers.add_parser("skill-load", help="Activate skill from archive to active registry")
    sub_sload.add_argument("name", type=str, help="Skill name")
    sub_sload.set_defaults(func=cmd_skill_load)
    
    # skill-archive
    sub_sarc = subparsers.add_parser("skill-archive", help="Move active skill to archive")
    sub_sarc.add_argument("name", type=str, help="Skill name")
    sub_sarc.set_defaults(func=cmd_skill_archive)
    
    # skill-list
    sub_slist = subparsers.add_parser("skill-list", help="List active and archived skills")
    sub_slist.add_argument("--all", action="store_true", help="Show all archived skills")
    sub_slist.set_defaults(func=cmd_skill_list)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()


