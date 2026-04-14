---
name: review-changes
description: git diffの変更内容をレビューし、問題点・改善点を指摘する
user-invocable: true
argument-hint: "[branch or commit range, default: staged + unstaged]"
context: fork
---

# 変更レビュースキル

現在の変更内容（またはブランチ間の差分）をレビューし、問題点を指摘する。

## 手順

1. 対象の差分を取得する
   - 引数なし: `git diff` + `git diff --cached` （ステージ済み＋未ステージ）
   - 引数あり: `git diff $ARGUMENTS`
2. 変更内容を以下の観点でレビューする:
   - バグ・ロジックエラー
   - セキュリティ上の問題（OWASP Top 10）
   - パフォーマンスへの影響
   - エッジケースの考慮漏れ
   - コードスタイル・可読性
3. レポートを出力する

## 出力フォーマット

```markdown
## レビュー結果

### 要約
変更ファイル数: N / 追加: +N / 削除: -N

### 指摘事項

#### [Critical] ファイル名:行番号
内容と修正案

#### [Warning] ファイル名:行番号
内容と修正案

#### [Info] ファイル名:行番号
内容

### 総評
（1-2文）
```

## ルール
- 重要度順に並べる（Critical > Warning > Info）
- 問題がなければ「指摘事項なし。LGTMです。」と出力する
- 日本語で出力する
- 些末なスタイル指摘は省く
