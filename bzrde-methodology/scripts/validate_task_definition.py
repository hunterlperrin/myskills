#!/usr/bin/env python3
"""
validate_task_definition.py — タスク定義書の構造的妥当性チェック

Usage:
    python3 scripts/validate_task_definition.py <path_to_task_definition.md>

Checks:
    1. Required sections exist
    2. Ambiguous words are flagged
    3. Confidence tags are present
    4. Confirmation rate is calculated and checked (threshold: 80%)
    5. Quality declaration section exists
    6. IP design table exists
"""

import sys
import re
from pathlib import Path


REQUIRED_SECTIONS = [
    ("目的", r"##?\s*(1\.)?\s*目的"),
    ("究極目的", r"###?\s*究極目的"),
    ("直接目的", r"###?\s*直接目的"),
    ("成果物", r"##?\s*(2\.)?\s*成果物"),
    ("要件", r"##?\s*(3\.)?\s*成果物が満たすべき要件|##?\s*(3\.)?\s*要件"),
    ("確認方法", r"##?\s*(4\.)?\s*要件を満たしているかの確認方法|##?\s*(4\.)?\s*確認方法"),
    ("IP設計", r"##?\s*(5\.)?\s*インタラクションポイント|##?\s*(5\.)?\s*IP"),
    ("タスクステップ", r"##?\s*(6\.)?\s*タスクステップ"),
]

AMBIGUOUS_WORDS_JP = [
    "適切に", "適切な", "正しく", "正しい",
    "必要に応じて", "〜的な", "〜など",
    "できるだけ", "なるべく", "しっかり",
    "きちんと", "ちゃんと", "うまく",
]

AMBIGUOUS_WORDS_EN = [
    "properly", "appropriately", "as needed",
    "if necessary", "adequate", "reasonable",
    "suitable", "etc.", "and so on",
]

CONFIDENCE_TAGS = ["確定", "仮説", "不明", "🅿️"]


def check_required_sections(content: str) -> list:
    issues = []
    for name, pattern in REQUIRED_SECTIONS:
        if not re.search(pattern, content):
            issues.append(f"FAIL: 必須セクション「{name}」が見つかりません")
    return issues


def check_ambiguous_words(content: str) -> list:
    issues = []
    all_ambiguous = AMBIGUOUS_WORDS_JP + AMBIGUOUS_WORDS_EN
    for word in all_ambiguous:
        matches = [m.start() for m in re.finditer(re.escape(word), content)]
        if matches:
            for pos in matches:
                line_num = content[:pos].count("\n") + 1
                issues.append(f"WARNING: 曖昧語「{word}」が{line_num}行目にあります")
    return issues


def check_confidence_tags(content: str) -> list:
    issues = []
    found_tags = [tag for tag in CONFIDENCE_TAGS if tag in content]
    if not found_tags:
        issues.append(
            "WARNING: 確信度タグ（確定/仮説/不明/🅿️）が1つも使われていません。"
            "情報の確実性を明示してください"
        )
    return issues


def check_confirmation_rate(content: str) -> list:
    issues = []
    # Match patterns like "10/15項目確定" or "XX/YY確定" or "= 67%"
    rate_pattern = r"(\d+)\s*/\s*(\d+)\s*項目確定|(\d+)\s*/\s*(\d+)\s*確定"
    matches = re.findall(rate_pattern, content)
    if not matches:
        issues.append(
            "INFO: 確定率（XX/YY項目確定）の記載がありません。"
            "初期段階では正常ですが、Planning移行前に追跡を開始してください"
        )
    else:
        for match in matches:
            confirmed = int(match[0] or match[2])
            total = int(match[1] or match[3])
            if total > 0:
                rate = confirmed / total * 100
                if rate < 80:
                    issues.append(
                        f"WARNING: 確定率 {confirmed}/{total} = {rate:.0f}% "
                        f"（80%未満。Planningフェーズ移行には80%以上が必要）"
                    )
                else:
                    issues.append(
                        f"PASS: 確定率 {confirmed}/{total} = {rate:.0f}%"
                    )
    return issues


def check_quality_declaration(content: str) -> list:
    issues = []
    quality_patterns = [
        r"品質基準", r"品質宣言", r"Quality",
    ]
    found = any(re.search(p, content) for p in quality_patterns)
    if not found:
        issues.append(
            "WARNING: 品質宣言/品質基準のセクションが見つかりません。"
            "各Phaseの冒頭で品質基準を宣言してください"
        )
    return issues


def check_ip_table(content: str) -> list:
    issues = []
    ip_pattern = r"IP[-#]?\s*\d|IP-0|IP-final"
    if not re.search(ip_pattern, content):
        issues.append(
            "WARNING: IP（インタラクションポイント）の定義が見つかりません。"
            "ユーザー確認のタイミングを設計してください"
        )
    return issues


def validate(filepath: str) -> dict:
    content = Path(filepath).read_text(encoding="utf-8")

    all_issues = []
    all_issues.extend(check_required_sections(content))
    all_issues.extend(check_ambiguous_words(content))
    all_issues.extend(check_confidence_tags(content))
    all_issues.extend(check_confirmation_rate(content))
    all_issues.extend(check_quality_declaration(content))
    all_issues.extend(check_ip_table(content))

    fails = [i for i in all_issues if i.startswith("FAIL")]
    warnings = [i for i in all_issues if i.startswith("WARNING")]
    passes = [i for i in all_issues if i.startswith("PASS")]
    infos = [i for i in all_issues if i.startswith("INFO")]

    status = "FAIL" if fails else ("WARNING" if warnings else "PASS")

    return {
        "status": status,
        "file": filepath,
        "summary": {
            "fail": len(fails),
            "warning": len(warnings),
            "pass": len(passes),
            "info": len(infos),
        },
        "issues": all_issues,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_task_definition.py <path_to_task_definition.md>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not Path(filepath).exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    result = validate(filepath)

    print(f"\n{'='*60}")
    print(f"  Task Definition Validation: {result['status']}")
    print(f"  File: {result['file']}")
    print(f"{'='*60}")
    print(f"  FAIL: {result['summary']['fail']}  "
          f"WARNING: {result['summary']['warning']}  "
          f"PASS: {result['summary']['pass']}  "
          f"INFO: {result['summary']['info']}")
    print(f"{'='*60}\n")

    for issue in result["issues"]:
        prefix = issue.split(":")[0]
        icon = {"FAIL": "❌", "WARNING": "⚠️", "PASS": "✅", "INFO": "ℹ️"}.get(prefix, "  ")
        print(f"  {icon} {issue}")

    print()
    sys.exit(0 if result["status"] != "FAIL" else 1)


if __name__ == "__main__":
    main()
