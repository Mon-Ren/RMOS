#!/usr/bin/env python3
"""KB Expand - 围绕指定主题批量扩展知识库。"""

import argparse
import subprocess
import sys
from pathlib import Path

VAULT = "vault"
TOOL = "scripts/obsidian_kb.py"


def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=".")
    return result.stdout.strip() + result.stderr.strip()


def main():
    parser = argparse.ArgumentParser(description="围绕主题批量扩展知识库")
    parser.add_argument("topic", help="核心主题")
    parser.add_argument("--subtopics", "-s", nargs="+", help="子主题列表")
    parser.add_argument("--type", "-t", default="concept", choices=["concept", "paper", "code", "project"])
    parser.add_argument("--vault", "-v", default=VAULT)
    parser.add_argument("--dry-run", action="store_true", help="只列出计划，不创建")
    args = parser.parse_args()

    print(f"📚 扩展计划: {args.topic}")
    print(f"{'=' * 50}")

    # 列出子主题
    subtopics = args.subtopics or []
    if not subtopics:
        print("⚠️  未指定子主题，请用 --subtopics 提供")
        print(f"   例: python3 scripts/kb_expand.py \"{args.topic}\" -s \"子主题1\" \"子主题2\"")
        sys.exit(1)

    print(f"核心主题: {args.topic}")
    print(f"子主题数: {len(subtopics)}")
    print()

    if args.dry_run:
        print("📝 计划创建的笔记:")
        for st in subtopics:
            print(f"  → {args.type}/{st}.md")
        print()
        print("提示: 去掉 --dry-run 执行创建")
        return

    # 创建笔记
    created = []
    for st in subtopics:
        cmd = f"python3 {TOOL} -v {args.vault} new \"{st}\" -t {args.type}"
        output = run(cmd)
        print(output)
        created.append(st)

    # 自动关联到核心主题
    print(f"\n🔗 建立链接到核心主题 [[{args.topic}]]:")
    for st in subtopics:
        cmd = f"python3 {TOOL} -v {args.vault} link \"{st}\" \"{args.topic}\""
        output = run(cmd)
        if output:
            print(output)

    # 更新 MOC
    print("\n📋 更新 MOC...")
    cmd = f"python3 {TOOL} -v {args.vault} moc"
    print(run(cmd))

    print(f"\n✅ 扩展完成: 创建了 {len(created)} 篇笔记")
    print("下一步: 填充每篇笔记的内容，补充更多链接")


if __name__ == "__main__":
    main()
