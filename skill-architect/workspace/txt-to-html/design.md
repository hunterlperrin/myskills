# Design: txt-to-html-presenter

## 1. File Structure

```
txt-to-html-presenter/
├── SKILL.md                          # ワークフロー定義 (~200行)
├── references/
│   ├── design-system.md              # ダーク・ミニマルデザイン仕様 (~100行)
│   ├── html-template.md              # HTMLテンプレート全文（ツールバー+コンテンツ+JS） (~200行)
│   └── conversion-rules.md           # ファイル形式別変換ルール（md/csv/txt） (~150行)
└── scripts/
    └── (なし — HTMLテンプレートはreferences/に、変換ロジックはClaudeの判断で実行)
```

**Design Test結果:**
- Test 1 (Same every time?): HTMLテンプレートの構造は固定だがコンテンツ依存部分が大きい → references/に記載、Claudeが適用
- Test 2 (Phase-specific?): デザイン仕様は生成時のみ必要 → 別ファイル
- Test 3 (Default unsatisfactory?): Yes — Claudeのデフォルト HTML出力はgenericすぎる → 明確なデザイン指針が必要
- Test 4 (Must NOT happen?): 外部依存、スクロール不可能なレイアウト、編集状態の永続化

**scripts/を置かない理由**: 変換対象のコンテンツは毎回異なり、Claudeが構造解析して適切なHTMLを生成する必要がある。決定論的スクリプトでは対応できない。

## 2. Workflow Design

**パターン: Sequential + Context-aware Selection**

```
Step 1: 入力解析 ─── ファイル読み取り + 形式判定
         │
Step 2: HTML生成 ─── references/読み込み → テンプレート適用 → コンテンツ変換
         │
Step 3: 出力 ─────── HTMLファイル書き出し + ブラウザで開く
```

### Step 1: 入力解析
- **Input**: ユーザーが指定したファイルパス（単一 or 複数）
- **Processing**:
  - ファイル読み取り
  - 拡張子 + 内容から形式判定（md/csv/txt/その他テキスト）
  - 構造解析（見出し、リスト、テーブル、コードブロック等の検出）
- **Output**: 解析済みコンテンツ + 形式情報
- **Transition**: 自動

### Step 2: HTML生成
- **Input**: 解析済みコンテンツ
- **Processing**:
  - `references/html-template.md` を読み込み
  - `references/design-system.md` を読み込み
  - `references/conversion-rules.md` を読み込み
  - テンプレートにコンテンツを埋め込み
  - JS機能（編集ON/OFF、sessionStorage、ダウンロード、画像ペースト）を含める
- **Output**: 完全なHTMLファイル内容
- **Transition**: 自動

### Step 3: 出力
- **Input**: HTMLファイル内容
- **Processing**:
  - 元ファイルと同じディレクトリに `[元ファイル名].html` として出力
  - `open` コマンドでブラウザ起動
- **Output**: HTMLファイル + ブラウザ表示
- **Transition**: 完了

## 3. Detection (Description Design)

### Frontmatter Description

```yaml
name: txt-to-html-presenter
description: >
  Convert text files (txt, md, csv) into styled, editable HTML documents
  for screen sharing and presentations. Use when the user wants to convert
  a text file to HTML, make a document presentable, create a shareable
  view of notes or data, or prepare content for screen sharing. Produces
  single self-contained HTML with dark minimal design, inline editing
  with sessionStorage auto-save, clipboard image paste, and download
  capability. Do NOT use for slide/presentation creation, PDF generation,
  or converting HTML to other formats.
```

### Tessle Discovery検証

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Specificity | 3/3 | "Convert text files", "inline editing", "clipboard image paste", "download" — 具体的アクション4つ |
| Completeness | 3/3 | WHAT: Convert text files to styled HTML / WHEN: "Use when...convert a text file to HTML, make a document presentable..." |
| Trigger Term Quality | 3/3 | "convert", "HTML", "presentable", "screen sharing", "shareable view" — 自然なユーザーフレーズ |
| Distinctiveness | 3/3 | "Do NOT use for slide/presentation creation, PDF generation" — 明確な除外条件 |

### Early Validation

**Should-trigger (5):**
1. 「このtxtをHTMLに変換して」
2. 「プレゼン用に見やすくして」
3. 「画面共有で見せたいからHTMLにして」
4. 「このcsvを見やすい形にして」
5. 「このメモをブラウザで見れるようにして」

**Should-NOT-trigger (5):**
1. 「スライドを作って」→ frontend-slides等のスライドスキル
2. 「PDFに変換して」→ PDF関連スキル
3. 「HTMLをtxtに変換して」→ 逆方向、対象外
4. 「Reactコンポーネントを作って」→ web-artifacts-builder
5. 「このHTMLのCSSを修正して」→ 既存HTML編集、変換ではない

## 4. Interaction Point Design

**ユーザーインタラクションなし（全自動）**

理由: このスキルは「ファイルを指定→HTML生成」の単方向変換。デザイン選択不要（ダーク・ミニマル固定）、構造判断はClaudeが自動実行。ユーザーの追加入力を求めるとワークフローが遅くなるだけ。

生成後にユーザーがブラウザで確認し、修正が必要なら「ここを直して」と指示するのが自然なフロー。

## 5. Prohibitions

- **外部依存禁止**: CDN、npm、Google Fonts等の外部リソースを読み込まない。全てインライン
- **localStorage禁止**: sessionStorageのみ使用（セッション終了で自動削除）
- **自動ダウンロード禁止**: ユーザーが明示的にボタンを押した場合のみ
- **過度な装飾禁止**: グラデーション背景、アニメーション、影の多用はミニマル原則に反する
- **元ファイルの変更禁止**: 入力ファイルは読み取り専用。HTMLは別ファイルとして出力

## 6. references/ 各ファイルの設計

### references/design-system.md
- CSS変数定義（色、フォント、スペーシング）
- ダーク・ミニマルの具体的ルール
- タイポグラフィ仕様（system-uiベース、可読性重視）
- ツールバーデザイン
- レスポンシブ対応指針

### references/html-template.md
- 完全なHTMLテンプレート（head/style/body/script）
- ツールバー: 編集ON/OFFトグル + ダウンロードボタン
- JS機能一覧:
  - 編集モード切替（contenteditable）
  - sessionStorage自動保存（debounce付き）
  - ページ読み込み時のsessionStorage復元
  - HTMLダウンロード（Blob生成）
  - クリップボード画像ペースト（Base64インライン）
  - 編集モード視覚フィードバック

### references/conversion-rules.md
- 形式判定ロジック（拡張子 + フォールバック内容解析）
- Markdown→HTML変換ルール（heading, list, code, blockquote, table, link, emphasis）
- CSV→HTML table変換ルール（ヘッダー行検出、セル整形）
- プレーンテキスト→HTML変換ルール（段落分割、空行処理）
- 複数ファイル入力時の結合ルール
