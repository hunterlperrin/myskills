---
name: find-skill
description: タスクや困りごとに合った公開スキル・プラグインを探し、評価・セットアップまで行う
user-invocable: true
argument-hint: <困っていること or やりたいこと>
allowed-tools: WebFetch, WebSearch, Bash, Read, Write, Glob, Grep, Agent
---

# スキル探索・セットアップスキル

ユーザーが困っていること・やりたいことに合った公開スキルやプラグインを探し、評価し、セットアップまで行う。

## 手順

### Step 1: 要件の整理とキーワード生成

`$ARGUMENTS` から以下を行う:

1. ユーザーが何を解決したいのかを1文で整理する
2. 検索用キーワードを **3〜5個** 生成する。以下の観点で多角的に作ること:
   - **直訳キーワード**: やりたいことをそのまま英語にしたもの（例: "code review", "test automation"）
   - **類義語・関連語**: 同じ意味の別の表現（例: "lint" ↔ "static analysis", "deploy" ↔ "CI/CD"）
   - **技術スタック固有語**: 特定の技術名が含まれる場合そのまま使う（例: "React", "PostgreSQL"）
   - **ワークフロー語**: 作業フローの段階を表す語（例: "planning", "debugging", "refactoring"）

例: 「テストが書けない」→ キーワード: `testing`, `TDD`, `test-driven`, `unit test`, `test generation`

### Step 2: 公開スキルの調査

生成したキーワードを使い、以下のソースを**並列で**調査する。各ソースに対して最も適切なキーワードを選んで使う。

#### ソース一覧

**Tier 1: 直接取得可能（WebFetch）**

1. **skills.sh** — Vercel運営の大規模スキルディレクトリ（9万以上）
   - `https://skills.sh` にアクセスし、関連スキルを探す
   - インストールは `npx skillsadd <owner/repo>` 形式

2. **awesome-skills.com** — キュレーション済みスキルディレクトリ（128以上）
   - `https://awesome-skills.com` にアクセスし、関連スキルを探す

3. **GitHub: travisvn/awesome-claude-skills** — 最大のキュレーションリスト（9.8k stars）
   - `https://raw.githubusercontent.com/travisvn/awesome-claude-skills/main/README.md` を取得して関連スキルを探す

4. **GitHub: anthropics/skills** — Anthropic公式スキル
   - `https://raw.githubusercontent.com/anthropics/skills/main/README.md` を取得して関連スキルを探す

5. **claude-plugins-official マーケットプレイス** — 公式プラグイン
   - `claude plugin search <キーワード>` で検索する（Bashツール使用）

**Tier 2: WebSearch経由（直接取得不可のため検索エンジン経由）**

6. **skillsmp.com** — 50万以上のスキルを集約したマーケットプレイス
   - 直接アクセスは403になるため、WebSearchで `site:skillsmp.com <キーワード>` を使って検索する
   - 個別スキルページ（`skillsmp.com/skills/...`）が見つかればWebFetchで詳細を取得する

7. **opencrew.ai** — マルチエージェントプラットフォーム
   - 直接アクセスはタイムアウトするため、WebSearchで `site:opencrew.ai skills <キーワード>` を使って検索する
   - スキル関連のページが見つかった場合のみ詳細を取得する

**Tier 3: 汎用Web検索（上記で不足の場合）**

8. **Web検索** — 上記で十分な候補が見つからない場合
   - WebSearchで `claude code skill <キーワード>` を検索する
   - 各キーワードで並列に検索し、結果を統合する

### Step 3: 候補の評価

見つかった候補を以下の基準で評価し、上位3つを選定する:

| 基準 | 重み |
|------|------|
| 目的との一致度 | 高 |
| GitHubスター数・インストール数・更新頻度 | 中 |
| SKILL.mdの品質（具体的な手順があるか） | 中 |
| セキュリティ（任意コード実行のリスク） | 高 |

### Step 4: レポート＆確認

以下のフォーマットでユーザーに提示し、**インストールするかどうか確認を取る**。

```markdown
## 見つかったスキル

> 検索キーワード: `keyword1`, `keyword2`, `keyword3`

### 1. [スキル名](リンク)
- 概要: ...
- 出典: skills.sh / awesome-skills.com / skillsmp.com / etc.
- 評価: ★★★★☆
- インストール方法: plugin / npx skillsadd / 手動コピー
- 備考: ...

### 2. ...
### 3. ...

---
どれをインストールしますか？（番号 or 「全部」 or 「やめる」）
```

### Step 5: セットアップ

ユーザーの選択に基づいてインストールを実行する。

**プラグインの場合:**
```bash
claude plugin install <name>@<marketplace>
```

**skills.sh経由の場合:**
```bash
npx skillsadd <owner/repo>
```

**スキル（SKILL.md）の場合:**
1. GitHubからSKILL.mdの内容を取得（WebFetch）
2. `~/.claude/skills/<skill-name>/SKILL.md` に保存
3. 補助ファイルがあればそれも取得・保存

**インストール後:**
- 使い方の簡単な例を提示する
- `/スキル名` の呼び出し例を示す

## ルール

- スキルの中身（SKILL.md）を読まずにインストールしない。必ず内容を確認する
- セキュリティリスクがあるスキル（任意コマンド実行、外部送信など）は警告する
- ユーザーの確認なしにインストールしない
- 日本語で応答する
- 見つからない場合は正直に「該当するスキルが見つかりませんでした」と報告する
