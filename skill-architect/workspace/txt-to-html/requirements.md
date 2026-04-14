# Requirements: txt-to-html-presenter

## Skill-or-not Filter
**Skill** — コンテキスト依存の変換手続き（構造解析・デザイン適用・JS機能埋め込み）でProgressive Disclosureが有効。

## Requirements

| # | Question | Answer |
|---|----------|--------|
| 1 | Purpose | Claude Codeが生成したtxt/md/csv等のファイルを、画面共有向けの見やすいHTMLに変換する。編集可能・デザイン統一・ダウンロード可能 |
| 2 | Trigger | 「HTMLに変換して」「プレゼン用に変換」「このtxtを見やすくして」「画面共有用にして」等 |
| 3 | Output | 単一HTMLファイル（CSS/JS埋め込み、外部依存なし） |
| 4 | Test cases | あり（txt/md/csv入力→HTML出力の検証が客観的に可能） |
| 5 | Quality criteria | ミニマル・ダーク系デザイン、編集ON/OFF、sessionStorage（タブ閉じで自動削除）、ダウンロード機能、画像ペースト対応 |
| 6 | Dependencies | なし（純粋HTML/CSS/JS、外部API不要） |

## Design Direction
- ミニマル・ダーク系
- 対応形式: txt, md, csv, その他テキスト系ファイル
- 編集: テキスト編集 + クリップボード画像ペースト（Base64インライン化）
- ダウンロード: HTML形式のみ
- ストレージ: sessionStorage（セッション終了で自動削除）

## Use Cases

### UC1: テキストファイルのプレゼン用HTML変換
- **Trigger**: 「このtxtをHTMLに変換して」「プレゼン用にして」
- **Steps**: ファイル読み取り → 構造解析（md: heading/list/code, csv: table, txt: paragraph） → ダークミニマルデザイン適用 → JS機能埋め込み → HTML出力
- **Result**: 編集可能・ダウンロード可能な単一HTMLファイル

### UC2: 画面共有中のリアルタイム編集
- **Trigger**: HTMLを開いて編集ボタンをON
- **Steps**: contenteditable有効化 → 画像ペースト対応 → 編集内容をsessionStorageに自動保存 → タブ/ブラウザ閉じで自動削除
- **Result**: 投影中にメモ・修正・画像貼り付けが可能、セッション中は内容保持

### UC3: 編集済みHTMLのローカル保存
- **Trigger**: ダウンロードボタン押下
- **Steps**: 現在のDOM状態をHTML化 → Blobで生成 → ダウンロードフォルダに保存
- **Result**: 編集内容が反映されたHTMLがローカルに永続保存
