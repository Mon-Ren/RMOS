#!/usr/bin/env python3
"""Obsidian KB - Bi-directional linked note knowledge base CLI."""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_VAULT = "vault"
TYPE_DIR_MAP = {
    "concept": "concepts",
    "paper": "papers",
    "code": "code",
    "project": "projects",
}


def get_vault(args):
    return Path(args.vault or DEFAULT_VAULT)


def today():
    return datetime.now().strftime("%Y-%m-%d")


def slugify(title):
    """Convert title to filename-safe slug."""
    s = title.lower().strip()
    s = re.sub(r"[^\w\u4e00-\u9fff\s-]", "", s)
    s = re.sub(r"[\s]+", "-", s)
    return s


def load_template(vault, note_type):
    tpl_path = vault / "_templates" / f"{note_type}.md"
    if tpl_path.exists():
        return tpl_path.read_text(encoding="utf-8")
    # fallback
    return (vault / "_templates" / "concept.md").read_text(encoding="utf-8")


def find_note(vault, title):
    """Find a note by title or filename (without .md)."""
    slug = slugify(title)
    for md in vault.rglob("*.md"):
        if md.name == f"{slug}.md" or md.stem == slug:
            return md
        # Check frontmatter title
        try:
            content = md.read_text(encoding="utf-8")
            m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
            if m and m.group(1).strip() == title.strip():
                return md
        except Exception:
            continue
    return None


def extract_wikilinks(content):
    """Extract all [[wikilink]] targets from content."""
    return re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", content)


def extract_frontmatter(content):
    """Extract YAML frontmatter as dict."""
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm


# ── Commands ──────────────────────────────────────────────


def cmd_new(args):
    """Create a new note from template."""
    vault = get_vault(args)
    note_type = args.type or "concept"
    title = args.title
    slug = slugify(title)

    target_dir = vault / TYPE_DIR_MAP.get(note_type, "concepts")
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{slug}.md"

    if target.exists():
        print(f"⚠️  笔记已存在: {target}")
        return

    tpl = load_template(vault, note_type)
    d = today()
    content = tpl.replace("{{title}}", title).replace("{{date}}", d)
    target.write_text(content, encoding="utf-8")
    print(f"✅ 创建: {target}")


def cmd_link(args):
    """Add a [[wikilink]] from source note to target note."""
    vault = get_vault(args)
    src = find_note(vault, args.source)
    tgt = find_note(vault, args.target)

    if not src:
        print(f"❌ 未找到笔记: {args.source}")
        return
    if not tgt:
        print(f"❌ 未找到笔记: {args.target}")
        return

    content = src.read_text(encoding="utf-8")
    link_text = f"[[{args.target}]]"

    if link_text in content:
        print(f"ℹ️  链接已存在: {args.source} → {args.target}")
        return

    # Append to ## 关联 section or create one
    if "## 关联" in content:
        content = re.sub(
            r"(## 关联\n)",
            r"\1" + f"- {link_text}\n",
            content,
        )
    else:
        content += f"\n## 关联\n- {link_text}\n"

    src.write_text(content, encoding="utf-8")
    print(f"🔗 链接: {args.source} → {args.target}")


def cmd_search(args):
    """Search notes by title, tags, or content."""
    vault = get_vault(args)
    query = args.query.lower()
    results = []

    for md in vault.rglob("*.md"):
        if md.name.startswith("_") or md.name == "MOC.md":
            continue
        try:
            content = md.read_text(encoding="utf-8")
        except Exception:
            continue

        fm = extract_frontmatter(content)
        title = fm.get("title", md.stem)
        tags = fm.get("tags", "")

        score = 0
        if query in title.lower():
            score += 3
        if query in tags.lower():
            score += 2
        if query in content.lower():
            score += 1

        if score > 0:
            # Extract first non-empty line as preview
            lines = content.split("\n")
            preview = ""
            for line in lines:
                line = line.strip()
                if line and not line.startswith("---") and not line.startswith("title:") and not line.startswith("tags:"):
                    preview = line[:80]
                    break
            results.append((score, title, str(md.relative_to(vault)), preview))

    results.sort(key=lambda x: -x[0])
    if not results:
        print("🔍 未找到匹配结果")
        return

    print(f"🔍 找到 {len(results)} 个结果:\n")
    for score, title, path, preview in results:
        print(f"  📄 {title}")
        print(f"     {path}")
        if preview:
            print(f"     {preview}")
        print()


def cmd_backlinks(args):
    """Find all notes that link to the target note."""
    vault = get_vault(args)
    target = args.title
    links = []

    for md in vault.rglob("*.md"):
        if md.name.startswith("_"):
            continue
        try:
            content = md.read_text(encoding="utf-8")
        except Exception:
            continue

        wikilinks = extract_wikilinks(content)
        if target in wikilinks:
            fm = extract_frontmatter(content)
            links.append(fm.get("title", md.stem))

    if not links:
        print(f"🔍 没有笔记引用 [[{target}]]")
        return

    print(f"📌 [[{target}]] 的反向链接 ({len(links)}):\n")
    for link in links:
        print(f"  ← {link}")


def cmd_moc(args):
    """Generate/update Map of Content."""
    vault = get_vault(args)
    sections = {}

    for note_type, dir_name in TYPE_DIR_MAP.items():
        dir_path = vault / dir_name
        if not dir_path.exists():
            continue
        notes = []
        for md in sorted(dir_path.glob("*.md")):
            fm = extract_frontmatter(md.read_text(encoding="utf-8"))
            title = fm.get("title", md.stem)
            tags = fm.get("tags", "")
            notes.append((title, tags))
        if notes:
            sections[note_type] = notes

    type_labels = {
        "concepts": "💡 概念",
        "papers": "📄 论文",
        "code": "💻 代码",
        "projects": "🚀 项目",
    }

    lines = [
        "---",
        f"title: Map of Content",
        f"updated: {today()}",
        "---",
        "",
        "# 🗺️ Map of Content",
        "",
        f"*最后更新: {today()}*",
        "",
    ]

    for dir_name, label in type_labels.items():
        if dir_name in sections:
            lines.append(f"## {label}")
            lines.append("")
            for title, tags in sections[dir_name]:
                tag_str = f" `{tags}`" if tags else ""
                lines.append(f"- [[{title}]]{tag_str}")
            lines.append("")

    moc_path = vault / "MOC.md"
    moc_path.write_text("\n".join(lines), encoding="utf-8")
    total = sum(len(v) for v in sections.values())
    print(f"✅ MOC 已更新: {total} 篇笔记")


def cmd_ask(args):
    """Search and retrieve context for LLM Q&A."""
    vault = get_vault(args)
    query = args.question.lower()

    # Score and collect relevant notes
    scored = []
    for md in vault.rglob("*.md"):
        if md.name.startswith("_") or md.name == "MOC.md":
            continue
        try:
            content = md.read_text(encoding="utf-8")
        except Exception:
            continue

        fm = extract_frontmatter(content)
        title = fm.get("title", md.stem)

        score = 0
        # Title match
        for word in query.split():
            if word in title.lower():
                score += 3
        # Tag match
        tags = fm.get("tags", "")
        for word in query.split():
            if word in tags.lower():
                score += 2
        # Content match
        for word in query.split():
            if len(word) > 1 and word in content.lower():
                score += 1

        if score > 0:
            # Expand context: find linked notes
            linked = extract_wikilinks(content)
            scored.append((score, title, content, linked))

    scored.sort(key=lambda x: -x[0])
    top = scored[:5]

    if not top:
        print("🔍 知识库中未找到相关内容")
        return

    print("=" * 60)
    print(f"📚 检索到 {len(top)} 篇相关笔记")
    print("=" * 60)

    for score, title, content, linked in top:
        print(f"\n{'─' * 40}")
        print(f"📄 {title} (相关度: {score})")
        print(f"{'─' * 40}")
        # Strip frontmatter for display
        clean = re.sub(r"^---\n.*?\n---\n", "", content, count=1, flags=re.DOTALL)
        print(clean)
        if linked:
            print(f"\n🔗 关联: {', '.join(linked)}")

    print(f"\n{'=' * 60}")
    print("以上内容可作为上下文提供给大模型进行问答")


def cmd_graph(args):
    """Show link graph as text."""
    vault = get_vault(args)
    graph = {}

    for md in vault.rglob("*.md"):
        if md.name.startswith("_") or md.name == "MOC.md":
            continue
        try:
            content = md.read_text(encoding="utf-8")
        except Exception:
            continue

        fm = extract_frontmatter(content)
        title = fm.get("title", md.stem)
        links = extract_wikilinks(content)
        if links:
            graph[title] = links

    if not graph:
        print("📊 暂无链接关系")
        return

    print("📊 笔记链接图:\n")
    for title, links in sorted(graph.items()):
        print(f"  {title}")
        for link in links:
            print(f"    └─→ [[{link}]]")
        print()


# ── Main ──────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Obsidian KB - 双链笔记知识库")
    parser.add_argument("--vault", "-v", help="Vault directory path")
    sub = parser.add_subparsers(dest="command")

    # new
    p_new = sub.add_parser("new", help="创建新笔记")
    p_new.add_argument("title", help="笔记标题")
    p_new.add_argument("--type", "-t", choices=["concept", "paper", "code", "project"], default="concept")

    # link
    p_link = sub.add_parser("link", help="添加双向链接")
    p_link.add_argument("source", help="源笔记标题")
    p_link.add_argument("target", help="目标笔记标题")

    # search
    p_search = sub.add_parser("search", help="搜索笔记")
    p_search.add_argument("query", help="搜索关键词")

    # backlinks
    p_bl = sub.add_parser("backlinks", help="查找反向链接")
    p_bl.add_argument("title", help="笔记标题")

    # moc
    sub.add_parser("moc", help="更新 MOC 索引")

    # ask
    p_ask = sub.add_parser("ask", help="知识库问答检索")
    p_ask.add_argument("question", help="问题")

    # graph
    sub.add_parser("graph", help="显示链接关系图")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "new": cmd_new,
        "link": cmd_link,
        "search": cmd_search,
        "backlinks": cmd_backlinks,
        "moc": cmd_moc,
        "ask": cmd_ask,
        "graph": cmd_graph,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
