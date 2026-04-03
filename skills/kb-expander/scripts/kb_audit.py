#!/usr/bin/env python3
"""KB Audit - 检查知识库的链接完整性和知识空白。"""

import re
import sys
from pathlib import Path
from collections import defaultdict

DEFAULT_VAULT = "vault"


def extract_wikilinks(content):
    return re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", content)


def extract_title(content):
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    return m.group(1).strip() if m else None


def main():
    vault = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(DEFAULT_VAULT)

    if not vault.exists():
        print(f"❌ Vault 不存在: {vault}")
        sys.exit(1)

    # 收集所有笔记
    notes = {}  # title -> path
    links_from = defaultdict(set)  # title -> set of linked titles
    link_count = defaultdict(int)  # how many times a title is linked

    for md in vault.rglob("*.md"):
        if md.name.startswith("_") or md.name == "MOC.md":
            continue
        try:
            content = md.read_text(encoding="utf-8")
        except Exception:
            continue

        title = extract_title(content) or md.stem
        notes[title] = md

        wikilinks = extract_wikilinks(content)
        for link in wikilinks:
            if link not in ("相关笔记1", "相关笔记2", "链接"):
                links_from[title].add(link)
                link_count[link] += 1

    print(f"📊 知识库审计报告")
    print(f"{'=' * 50}")
    print(f"总笔记数: {len(notes)}")
    print(f"总链接数: {sum(len(v) for v in links_from.values())}")
    print()

    # 1. 死链接：引用了但不存在的笔记
    all_titles = set(notes.keys())
    dead_links = set()
    for title, links in links_from.items():
        for link in links:
            if link not in all_titles:
                dead_links.add((title, link))

    if dead_links:
        print(f"🔗 死链接 ({len(dead_links)}) — 被引用但不存在的笔记:")
        for src, target in sorted(dead_links):
            print(f"  ⚠️  [[{src}]] → [[{target}]] (不存在)")
        print()
    else:
        print("✅ 没有死链接\n")

    # 2. 孤立笔记：没有链接任何其他笔记，也没有被链接
    isolated = []
    for title in all_titles:
        outgoing = len(links_from.get(title, set()))
        incoming = link_count.get(title, 0)
        if outgoing == 0 and incoming == 0:
            isolated.append(title)

    if isolated:
        print(f"🏝️  孤立笔记 ({len(isolated)}) — 无任何链接:")
        for title in sorted(isolated):
            print(f"  📄 {title}")
        print()
    else:
        print("✅ 没有孤立笔记\n")

    # 3. 只出不入的笔记：链接了别人但没人链接它
    one_way = []
    for title in all_titles:
        outgoing = len(links_from.get(title, set()))
        incoming = link_count.get(title, 0)
        if outgoing > 0 and incoming == 0:
            one_way.append((title, outgoing))

    if one_way:
        print(f"📤 只出不入 ({len(one_way)}) — 链接了别人但没人链接它:")
        for title, count in sorted(one_way, key=lambda x: -x[1]):
            print(f"  📄 {title} (发出 {count} 个链接)")
        print()

    # 4. 最被引用的笔记
    if link_count:
        print("🏆 最被引用的笔记 (Top 10):")
        for title, count in sorted(link_count.items(), key=lambda x: -x[1])[:10]:
            exists = "✅" if title in all_titles else "❌"
            print(f"  {exists} [[{title}]] — 被引用 {count} 次")
        print()

    # 5. 扩展建议
    print("💡 扩展建议:")
    if dead_links:
        targets = set(t for _, t in dead_links)
        print(f"  优先创建以下 {len(targets)} 篇被引用的缺失笔记:")
        for t in sorted(targets):
            refs = [s for s, l in dead_links if l == t]
            print(f"    → [[{t}]] (被 {', '.join(refs)} 引用)")
    elif isolated:
        print(f"  给 {len(isolated)} 篇孤立笔记添加关联")
    else:
        print("  知识库链接完整，考虑扩展新主题或深化已有主题")


if __name__ == "__main__":
    main()
