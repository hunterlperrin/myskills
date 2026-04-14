---
name: bzrde-methodology
description: >
  にからすの仕事の方法論。タスク定義書の作成、仮説ベース情報処理、
  仕様書作成、リサーチ、報告書作成、プロジェクト管理をカバーする。
  Use when starting any task, writing specs, conducting research,
  creating reports, or managing projects. Also use when user says
  "方法論で" "ゴールデンルールで" "にからすのやり方で"
  "タスク定義書を作って" "仕様書を書いて" "リサーチして" "報告書を作って".
  Do NOT use for executing domain tasks like coding, design, or data analysis.
---

# BZRDE Methodology — にからすの方法論

小竹泉里（BZRDE）が60件以上のプロジェクトで確立した仕事の方法論。タスクの種別を判定し、適切な手法を動的にロードして実行する。にからすのSpec-Driven Development: タスク定義書が全ての起点であり、ソースオブトゥルース。

**v3.1 更新内容（2026-03-23）**: 感情曲線設計フレームワーク追加（reporting.md §3）、盲点探索ステップ明示化（structuring.md Step 4.5、spec-writing.md §4）、杉江商会トンマナ追加。

## Core Protocol（全タスク共通 — 暗記レベル）

### 1. タスク定義書を最初に作れ

定義書なしに動くな。テンプレートは `references/core-principles.md` §1。

```
究極目的 → 直接目的 → 成果物 → 要件 → 確認方法 → IP設計 → タスクステップ
```

### 2. 品質宣言→検証サイクル

各Phaseの冒頭で品質基準を宣言。Phase完了時にPASS/FAILで検証。FAILなら修正してから次へ。宣言なしで着手するな。

### 3. 成果物から逆算

最終成果物のフォーマットを先に確定 → 必要な情報を特定 → 論点を導出 → 情報収集を設計。ゴールのない調査はしない。

### 4. 仮説ベース処理

情報を扱うときは常に確信度を明示する:
- **確定**: ソースで明示的に確認済み
- **仮説**: 推論に基づく。検証が必要
- **不明**: 情報不足
- **🅿️**: 後日確認が必要

確定率を「XX/YY項目確定」で追跡する。

### 5. IPを設計する

フェーズの切れ目で必ずユーザー確認を入れる。確認なしで次フェーズに進むな。

---

## Task Type Router

タスクを受け取ったら、まずここで種別を判定する。

### Step 1 — 常に最初にやること

`references/core-principles.md` を読む。全タスクで必須。

### Step 2 — プロジェクトフェーズを判定

| 今の状態 | フェーズ | 読むファイル |
|---------|---------|------------|
| 構想・アイデア・書き起こしがある。何を作るかまだ曖昧 | **Discovery** | `references/structuring.md` |
| 方向性は決まった。市場・技術・競合の情報が足りない | **Research** | `references/research-flow.md` |
| 情報は揃った。計画・設計・仕様を書く段階 | **Planning** | `references/spec-writing.md` |
| 計画は動いている。進捗管理・課題対応が必要 | **Execution** | `references/project-management.md` |
| 成果を報告・提案する段階 | **Delivery** | `references/reporting.md` |

多くのタスクは複数フェーズにまたがる。該当する全ファイルを読む。

### Step 3 — アウトプットの性質を判定

| アウトプット | テンプレート元 |
|------------|--------------|
| プロジェクト計画（ロードマップ、WBS） | `references/spec-writing.md` §層1 |
| 事業計画/戦略（市場分析、GTM、Go/No-Go） | `references/spec-writing.md` §層2 |
| システム/ソフトウェア仕様 | `references/spec-writing.md` §層3 |
| 調査レポート | `references/research-flow.md` §受容フレームワーク |
| クライアント報告書 | `references/reporting.md` |

計画書も事業計画もシステム仕様も、全て「仕様書」の広義の形態。

### Step 4 — 判定に迷ったら

ユーザーに聞く:
1. 「今どのフェーズにいますか？」
2. 「最終的に何を作りますか？」

推測で進めるな。

### Step 5 — 失敗時の戻り先

| 現在フェーズ | 失敗条件 | 戻り先 |
|------------|---------|--------|
| Discovery | タスク定義書が却下された | Discovery冒頭 |
| Research | 仮説が全て棄却、方向性が変わった | Discovery |
| Planning | 確定率80%に達しない | Research |
| Execution | ブロッカーが技術的壁 | Planning |
| Delivery | クライアントが報告内容を却下 | Planning or Research |

---

## Quick Reference — Output Format Guide

| やりたいこと | Output / 出力形式 | 読むファイル |
|-------------|---------|------------|
| 会議書き起こしから構造化 | タスク定義書(md) + 論点リスト | core-principles → structuring |
| 市場調査・仮説検証 | 仮説検証結果表 + 受容FW | core-principles → research-flow |
| プロジェクト計画を書く | 計画書(md) | core-principles → spec-writing §層1 |
| 事業計画・戦略を書く | 事業計画書(md) | core-principles → spec-writing §層2 |
| システム仕様を書く | 仕様書6点セット(md) | core-principles → spec-writing §層3 |
| プロジェクトを管理 | 進捗テーブル + ブロッカーリスト | core-principles → project-management |
| クライアント報告書を作成 | 報告書(docx/pptx) | core-principles → reporting |
| 提案・セールス資料を作る | 提案書(pptx) + 感情曲線設計書(md) | core-principles → reporting §3（感情曲線設計） |
| タスク定義書の品質チェック | 検証結果(stdout) | `scripts/validate_task_definition.py` |

---

## Forbidden Patterns

- タスク定義書なしで作業を開始する
- 仮説と事実を区別せずに結論を出す
- 品質基準を宣言せずにPhaseに着手する
- IPなしで長時間の作業を進める
- 曖昧語（「適切に」「〜的な」「〜など」等）を要件に含める
- 推測で情報を補完する（不明なら質問する）

---

## Troubleshooting

| 問題 | 対策 |
|------|------|
| どのフェーズかわからない | Step 4の2つの質問をユーザーに聞く |
| 複数フェーズにまたがる | 該当する全ファイルを読む。Discoveryから順に進める |
| 確定率が上がらない | 確認先を分散する。1人に全部聞くな |
| テンプレートに合わない | 無理に押し込まない。テンプレートはガイドであり制約ではない |

---

## PJ固有の上書き

グローバル版: `~/.claude/skills/bzrde-methodology/`

PJ固有の追加指示は `.claude/skills/bzrde-methodology/` に配置する。クライアント固有のトンマナやテンプレートの上書きが可能。

```
.claude/skills/bzrde-methodology/
└── references/
    └── client-tonmana.md    # クライアント固有のトンマナルール
```

---

## References

読むタイミングを守ること。全部を一度に読むな。

- Read `references/core-principles.md` first for every task. タスク定義書、仮説ベース処理、品質管理、IP設計、成果物逆算、AI指示原則。
- Read `references/structuring.md` at Discovery. 曖昧な構想を構造化する手法。
- Read `references/research-flow.md` at Research. 仮説駆動の調査手法とDeep Research設計。
- Read `references/spec-writing.md` at Planning. 3層テンプレートと論点管理。
- Read `references/reporting.md` at Delivery. 報告書パターンとトンマナ。
- Read `references/project-management.md` at Execution. 進捗追跡とフリーズ対策。
