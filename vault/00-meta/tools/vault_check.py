#!/usr/bin/env python3
"""vault_check — keep the MSLD vault consistent (stdlib only).

Usage (from the repository root or anywhere):
    python vault/00-meta/tools/vault_check.py            # check links + frontmatter, refresh indexes
    python vault/00-meta/tools/vault_check.py --check    # check only, do not rewrite dashboards
    python vault/00-meta/tools/vault_check.py --next TASK   # print the next free ID (TASK, REQ, ADR, ...)

What it does
  1. every [[wikilink]] and ![[embed]] must resolve to a note or an attachment;
  2. ID notes: the file name starts with the frontmatter id; type and status are allowed values;
  3. link fields in frontmatter ("[[...]]" strings) must resolve;
  4. regenerates the static tables between <!-- BEGIN GENERATED --> and <!-- END GENERATED --> in
     01-dashboards (Task board, Issue tracker, Requirements index, Feature list).
Exit code 1 if any problem was found.
"""
import os
import re
import sys

VAULT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ID_RE = re.compile(r"^(G|UC|REQ|FEAT|TASK|ISS|ADR|EXP|AUD)-(\d+)$")
LINK_RE = re.compile(r"(!?)\[\[([^\]\|#]*?)\\?(#[^\]\|]*)?(\\?\|[^\]]*)?\]\]")

STATUSES = {
    "goal": {"active", "achieved", "dropped"},
    "use-case": {"active", "dropped"},
    "requirement": {"proposed", "approved", "partial", "implemented", "verified", "deferred", "rejected"},
    "feature": {"planned", "in-progress", "done", "needs-rework", "deferred", "dropped"},
    "task": {"todo", "doing", "blocked", "review", "done", "cancelled"},
    "issue": {"open", "investigating", "fixed", "wontfix", "duplicate"},
    "adr": {"proposed", "accepted", "superseded", "deprecated", "rejected"},
    "experiment": {"planned", "running", "done"},
    "audit": {"planned", "done"},
    "theory": {"draft", "reviewed"},
    "reference": {"draft", "verified"},
    "subsystem": {"target", "as-built", "partial", "planned"},
    "component": {"target", "as-built", "partial", "planned"},
    "contract": {"target", "as-built", "partial", "planned"},
}
PREFIX_TYPE = {"G": "goal", "UC": "use-case", "REQ": "requirement", "FEAT": "feature", "TASK": "task",
               "ISS": "issue", "ADR": "adr", "EXP": "experiment", "AUD": "audit"}


def read_notes():
    notes = {}
    attachments = set()
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            path = os.path.join(root, f)
            if f.endswith(".md"):
                notes[f[:-3]] = path
            else:
                attachments.add(f)
    return notes, attachments


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    fm = {}
    for line in text[4:end].split("\n"):
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            if '"' in inner:
                fm[key] = re.findall(r'"([^"]*)"', inner)
            else:
                fm[key] = [x.strip() for x in inner.split(",") if x.strip()]
        else:
            fm[key] = val.strip('"')
    return fm, text[end + 5:]


def label(v):
    """'[[REQ-001 Title|REQ-001]]' -> 'REQ-001'; plain -> itself."""
    m = re.match(r"^\[\[([^\]\|]*)(\|([^\]]*))?\]\]$", v)
    if not m:
        return v
    return m.group(3) or m.group(1)


def as_list(v):
    if v is None or v == "":
        return []
    return v if isinstance(v, list) else [v]


def main(argv):
    notes, attachments = read_notes()
    problems = []
    meta = {}
    for stem, path in notes.items():
        text = open(path, encoding="utf-8").read()
        fm, body = parse_frontmatter(text)
        meta[stem] = (fm, path)
        rel = os.path.relpath(path, VAULT)
        if "00-meta/templates" in rel.replace(os.sep, "/"):
            continue
        # links (body + frontmatter)
        for m in LINK_RE.finditer(text):
            target = m.group(2).strip().rstrip("\\")
            if not target:
                continue
            if m.group(1) == "!":
                if target not in attachments and target not in notes:
                    problems.append(f"{rel}: missing embed [[{target}]]")
            elif target not in notes:
                problems.append(f"{rel}: broken link [[{target}]]")
        # frontmatter sanity
        nid = fm.get("id")
        typ = fm.get("type")
        if nid:
            mm = ID_RE.match(nid)
            if not mm:
                problems.append(f"{rel}: malformed id {nid!r}")
            else:
                if not stem.startswith(nid + " ") and stem != nid:
                    problems.append(f"{rel}: file name does not start with id {nid}")
                want = PREFIX_TYPE[mm.group(1)]
                if typ != want:
                    problems.append(f"{rel}: id {nid} but type {typ!r} (expected {want!r})")
        if typ in STATUSES and fm.get("status") not in STATUSES[typ]:
            problems.append(f"{rel}: status {fm.get('status')!r} not allowed for type {typ!r}")

    if len(argv) >= 2 and argv[0] == "--next":
        prefix = argv[1].upper()
        nums = [int(ID_RE.match(fm.get("id", "")).group(2)) for fm, _ in meta.values()
                if fm.get("id", "").startswith(prefix + "-") and ID_RE.match(fm.get("id", ""))]
        width = 4 if prefix == "ADR" else (1 if prefix in ("G", "UC") else 3)
        print(f"{prefix}-{(max(nums) + 1 if nums else 1):0{width}d}")
        return 0

    by_type = {}
    for stem, (fm, path) in meta.items():
        by_type.setdefault(fm.get("type"), []).append((fm.get("id", ""), stem, fm))
    for v in by_type.values():
        v.sort()

    def link(stem, text=None):
        return f"[[{stem}\\|{text}]]" if text else f"[[{stem}]]"

    def cell(v):
        """a frontmatter value -> table cell text; links keep working (pipe escaped)."""
        m = re.match(r"^\[\[([^\]\|]*)(\|([^\]]*))?\]\]$", v)
        if not m:
            return v
        return link(m.group(1), m.group(3))

    def ids(values):
        return ", ".join(cell(x) for x in as_list(values)) or "—"

    tables = {}
    # Task board
    order = ["doing", "review", "blocked", "todo", "done", "cancelled"]
    lines = []
    for st in order:
        rows = [r for r in by_type.get("task", []) if r[2].get("status") == st]
        if st in ("todo",):
            rows.sort(key=lambda r: (r[2].get("priority", "P9"), r[0]))
        if not rows:
            continue
        lines.append(f"\n### {st} ({len(rows)})\n")
        lines.append("| task | title | priority | milestone | feature |")
        lines.append("|---|---|---|---|---|")
        for nid, stem, fm in rows:
            lines.append(f"| {link(stem, nid)} | {fm.get('title','')} | {fm.get('priority','')} | "
                         f"{fm.get('milestone','')} | {ids(fm.get('feature'))} |")
    tables["Task board"] = "\n".join(lines)
    # Issues
    sev = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    rows = sorted(by_type.get("issue", []), key=lambda r: (r[2].get("status") in ("fixed", "wontfix", "duplicate"),
                                                         sev.get(r[2].get("severity"), 9), r[0]))
    lines = ["| issue | title | status | severity | kind | confidence | fixed by |", "|---|---|---|---|---|---|---|"]
    for nid, stem, fm in rows:
        lines.append(f"| {link(stem, nid)} | {fm.get('title','')} | {fm.get('status','')} | {fm.get('severity','')} | "
                     f"{fm.get('kind','')} | {fm.get('confidence','')} | {ids(fm.get('fixed_by'))} |")
    tables["Issue tracker"] = "\n".join(lines)
    # Requirements
    lines = ["| req | title | area | priority | status | satisfied by | verified by |",
             "|---|---|---|---|---|---|---|"]
    for nid, stem, fm in by_type.get("requirement", []):
        lines.append(f"| {link(stem, nid)} | {fm.get('title','')} | {fm.get('area','')} | {fm.get('priority','')} | "
                     f"{fm.get('status','')} | {ids(fm.get('satisfied_by'))} | {ids(fm.get('verified_by'))} |")
    tables["Requirements index"] = "\n".join(lines)
    # Features
    lines = ["| feature | title | status | milestone | implements | open issues |", "|---|---|---|---|---|---|"]
    for nid, stem, fm in by_type.get("feature", []):
        lines.append(f"| {link(stem, nid)} | {fm.get('title','')} | {fm.get('status','')} | {fm.get('milestone','')} | "
                     f"{ids(fm.get('implements'))} | {ids(fm.get('issues'))} |")
    tables["Feature list"] = "\n".join(lines)

    if "--check" not in argv:
        for name, table in tables.items():
            path = notes.get(name)
            if not path:
                continue
            text = open(path, encoding="utf-8").read()
            new = re.sub(r"<!-- BEGIN GENERATED -->.*?<!-- END GENERATED -->",
                         lambda _m: "<!-- BEGIN GENERATED -->\n" + table.strip("\n") + "\n<!-- END GENERATED -->",
                         text, flags=re.S)
            if new != text:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)

    counts = {t: len(v) for t, v in by_type.items() if t}
    print(f"vault: {VAULT}")
    print("notes:", len(notes), " ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    for p in problems:
        print("PROBLEM:", p)
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
