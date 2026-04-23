#!/usr/bin/env python3
"""
executor.py — MeridianSignal Pipeline Stage 8 Executor
Wraps Aider in architect mode to execute plan.md task-by-task.

Usage:
    python executor.py --plan ./plan.md --design ./design.md --task P1-T1
    python executor.py --plan ./plan.md --design ./design.md --phase P1
    python executor.py --plan ./plan.md --design ./design.md --auto

Contract:
- One Aider invocation per Task ID.
- Each task run is non-interactive (--message flag).
- No auto-commits; the wrapper commits only after the task report verifies.
- Stops on first DEVIATED/BLOCKED/ESCALATION report.
- Writes every task report to ./reports/<task_id>.md.
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys, time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

AIDER_BIN = os.environ.get("AIDER_BIN", "aider")
AIDER_MODEL = os.environ.get("AIDER_MODEL", "deepseek/deepseek-chat")
REPORTS_DIR = Path("./reports")
TASK_ID_RE = re.compile(r"^P(\d+)-T(\d+)$")

# ---------- plan.md parser ----------

@dataclass
class Task:
    id: str
    name: str
    description: str
    inputs: str
    outputs: str
    dependencies: list[str] = field(default_factory=list)
    complexity: str = "Medium"
    owner_type: str = "Full-stack"
    phase: str = ""

def parse_plan(plan_md: str) -> list[Task]:
    """Extract tasks from plan.md Section 2 (Phase Task Breakdown)."""
    tasks: list[Task] = []
    current_phase = ""
    block: dict[str, str] = {}
    for line in plan_md.splitlines():
        phase_match = re.match(r"^###\s+Phase\s+(P\d+)", line)
        if phase_match:
            current_phase = phase_match.group(1)
            continue
        m = re.match(r"^-\s*(Task ID|Task name|Description|Inputs|Expected output|Dependencies|Complexity|Owner type)\s*:\s*(.*)$", line, re.I)
        if m:
            block[m.group(1).lower()] = m.group(2).strip()
            continue
        if line.strip() == "" and block.get("task id"):
            tid = block["task id"].strip()
            if TASK_ID_RE.match(tid):
                tasks.append(Task(
                    id=tid,
                    name=block.get("task name", ""),
                    description=block.get("description", ""),
                    inputs=block.get("inputs", ""),
                    outputs=block.get("expected output", ""),
                    dependencies=[d.strip() for d in re.split(r"[,\s]+", block.get("dependencies", "")) if TASK_ID_RE.match(d.strip())],
                    complexity=block.get("complexity", "Medium"),
                    owner_type=block.get("owner type", "Full-stack"),
                    phase=current_phase or tid.split("-")[0],
                ))
            block = {}
    return tasks

# ---------- report store ----------

def load_completed() -> set[str]:
    REPORTS_DIR.mkdir(exist_ok=True)
    done = set()
    for p in REPORTS_DIR.glob("*.md"):
        text = p.read_text()
        m = re.search(r"^Status:\s*(COMPLETE)\b", text, re.M)
        if m:
            done.add(p.stem)
    return done

def save_report(task_id: str, report: str) -> Path:
    REPORTS_DIR.mkdir(exist_ok=True)
    p = REPORTS_DIR / f"{task_id}.md"
    p.write_text(report)
    return p

# ---------- Aider invocation ----------

def build_prompt(task: Task, design_md: str, plan_md: str, prior_reports: str) -> str:
    """Compose the exact message sent to Aider. Mirrors executor_agent.md contract."""
    return f"""You are the MeridianSignal Executor. Follow executor_agent.md strictly.

=== CURRENT TASK ===
Task ID: {task.id}
Task Name: {task.name}
Phase: {task.phase}
Complexity: {task.complexity}
Owner Type: {task.owner_type}

Description:
{task.description}

Inputs required:
{task.inputs}

Expected output:
{task.outputs}

Dependencies (must already be COMPLETE): {', '.join(task.dependencies) or 'None'}

=== PRIOR TASK REPORTS ===
{prior_reports or 'None — this is the first task.'}

=== DESIGN (read-only reference) ===
{design_md}

=== PLAN (authoritative) ===
{plan_md}

=== INSTRUCTIONS ===
1. Execute ONLY {task.id}. Do not touch adjacent tasks.
2. Do not make design decisions. Escalate ambiguity.
3. On completion, emit a Task Report using the exact format from executor_agent.md.
4. Do not commit. The wrapper commits on your behalf after verification.
"""

def run_aider(prompt: str, repo_path: Path) -> tuple[int, str]:
    """Invoke Aider non-interactively. Returns (exit_code, combined_stdout_stderr)."""
    cmd = [
        AIDER_BIN,
        "--architect",
        "--model", AIDER_MODEL,
        "--no-auto-commits",
        "--no-pretty",
        "--yes-always",
        "--message", prompt,
    ]
    proc = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, timeout=60*30)
    return proc.returncode, proc.stdout + "\n" + proc.stderr

# ---------- report verification ----------

REPORT_RE = re.compile(r"TASK REPORT.*?Awaiting:\s*(GO|RESOLVE|DECISION)[^\n]*", re.S)

def extract_report(aider_output: str) -> Optional[str]:
    m = REPORT_RE.search(aider_output)
    return m.group(0) if m else None

def report_status(report: str) -> str:
    m = re.search(r"^Status:\s*(COMPLETE|DEVIATED|BLOCKED|ESCALATION NEEDED)", report, re.M)
    return m.group(1) if m else "UNKNOWN"

# ---------- git commit ----------

def commit_task(repo_path: Path, task: Task) -> None:
    subprocess.run(["git", "add", "-A"], cwd=repo_path, check=True)
    msg = f"{task.id}: {task.name}"
    subprocess.run(["git", "commit", "-m", msg, "--allow-empty"], cwd=repo_path, check=True)

# ---------- orchestrator ----------

def execute(task: Task, plan_md: str, design_md: str, repo_path: Path) -> str:
    """Run a single task. Returns the status string."""
    completed = load_completed()
    missing_deps = [d for d in task.dependencies if d not in completed]
    if missing_deps:
        status = "BLOCKED"
        report = f"TASK REPORT\nTask ID: {task.id}\nStatus: BLOCKED\nBlockers: missing dependencies {missing_deps}\nAwaiting: RESOLVE dependencies\n"
        save_report(task.id, report)
        return status

    prior = "\n\n".join(sorted([p.read_text() for p in REPORTS_DIR.glob("*.md")]))
    prompt = build_prompt(task, design_md, plan_md, prior)
    code, output = run_aider(prompt, repo_path)
    report = extract_report(output) or f"TASK REPORT\nTask ID: {task.id}\nStatus: ESCALATION NEEDED\nBlockers: Aider produced no parseable report (exit {code})\nAwaiting: RESOLVE\n"
    save_report(task.id, report)
    status = report_status(report)
    if status == "COMPLETE":
        commit_task(repo_path, task)
    return status

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True, type=Path)
    ap.add_argument("--design", required=True, type=Path)
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--task", help="Single Task ID, e.g. P1-T1")
    g.add_argument("--phase", help="All tasks in a phase, e.g. P1")
    g.add_argument("--auto", action="store_true", help="Run full plan until blocker")
    args = ap.parse_args()

    plan_md = args.plan.read_text()
    design_md = args.design.read_text()
    all_tasks = parse_plan(plan_md)
    if not all_tasks:
        print("ERROR: no tasks parsed from plan.md", file=sys.stderr)
        return 2

    if args.task:
        targets = [t for t in all_tasks if t.id == args.task]
    elif args.phase:
        targets = [t for t in all_tasks if t.phase == args.phase]
    else:
        targets = all_tasks

    if not targets:
        print("ERROR: no matching tasks", file=sys.stderr)
        return 2

    for t in targets:
        print(f"[executor] running {t.id} — {t.name}")
        status = execute(t, plan_md, design_md, args.repo)
        print(f"[executor] {t.id} -> {status}")
        if status != "COMPLETE":
            print(f"[executor] stopping: {t.id} returned {status}. See reports/{t.id}.md")
            return 1
    print("[executor] all targeted tasks COMPLETE")
    return 0

if __name__ == "__main__":
    sys.exit(main())
