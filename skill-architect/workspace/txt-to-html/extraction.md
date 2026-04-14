# Knowledge Extraction: txt-to-html-presenter

## 1. Structure Patterns

| Element | Source | Use method |
|---------|--------|------------|
| 単一HTML・ゼロ依存（CSS/JS全インライン） | frontend-slides | As-is |
| Progressive Disclosure: SKILL.md→references/→scripts/ | agentskills.io spec | As-is |
| SKILL.md ≤500行、詳細はreferences/に分離 | agentskills.io spec | As-is |
| フェーズ制ワークフロー（検出→変換→出力） | frontend-slides Phase 0-5 | Adapt: スライド向け6フェーズ→ドキュメント向け3ステップに簡略化（入力解析→HTML生成→出力） |
| デザイン定義を別ファイルに分離 | frontend-slides STYLE_PRESETS.md | Adapt: プリセット選択不要（ダーク・ミニマル一択）だが、デザイン仕様はreferences/に分離 |

## 2. Code Fragments

| Element | Source | Use method |
|---------|--------|------------|
| contenteditable ON/OFF切替 | frontend-slides (inline editing) | Adapt: localStorage→sessionStorageに変更、トグルボタンUIを明示的に |
| Blob生成→ダウンロード | 汎用Webパターン | As-is: `new Blob([html], {type:'text/html'})` → `URL.createObjectURL` → `a.click()` |
| クリップボード画像ペースト | 汎用Webパターン | As-is: `paste`イベント → `clipboardData.items` → `FileReader.readAsDataURL` → Base64 img挿入 |
| sessionStorage自動保存 | 汎用Webパターン | As-is: `input`イベントでdebounce保存、`beforeunload`不要（sessionStorageはタブ閉じで自動削除） |
| CSS変数によるテーマ一元管理 | frontend-slides `:root` vars | As-is |

## 3. Concepts & Principles

| Element | Source | Use method |
|---------|--------|------------|
| "AI slop"回避 — generic aesthetic排除 | frontend-slides | Adapt: スライドほど派手にせず、ミニマル・ダーク文脈での「generic回避」に限定（過度な装飾・gradientを避ける） |
| ゼロ依存原則 — 外部CDN/npm不使用 | frontend-slides | As-is |
| コンテンツ密度制限 | frontend-slides (viewport fitting) | Adapt: スライド制約ではなくドキュメントとしての可読性ルール（行間・フォントサイズ・マージン） |
| description = トリガーの全責任を負う | agentskills.io spec, survey-methodology | As-is |

## 4. Templates

| Element | Source | Use method |
|---------|--------|------------|
| HTMLテンプレート構造（head→style→body→script） | frontend-slides html-template.md | Adapt: スライド構造→ドキュメント構造に。nav(ツールバー) + main(コンテンツ) + script(機能) |
| フロントマター形式 | agentskills.io spec | As-is: `name`, `description` required, `metadata` optional |
| ファイル形式別パーサーテンプレート | 独自設計 | 新規: md→heading/list/code/table、csv→table、txt→paragraph |

## 5. Quality Criteria

| Element | Source | Use method |
|---------|--------|------------|
| SKILL.md ≤500行 | agentskills.io spec | As-is |
| name: lowercase+hyphens, ≤64chars | agentskills.io spec | As-is |
| description: ≤1024chars, WHAT+WHEN | agentskills.io spec | As-is |
| 生成HTMLの検証: 構文正当性、機能動作 | skill-architect QA pipeline | As-is |

---

## Integration Table

| Element | Target Phase | Use method |
|---------|-------------|------------|
| ファイル形式判定（拡張子+内容解析） | 変換処理 | 新規実装 |
| Markdown→HTML構造変換ルール | references/conversion-rules.md | 新規実装 |
| CSV→tableレンダリングルール | references/conversion-rules.md | 新規実装 |
| ダーク・ミニマルデザイン仕様 | references/design-system.md | Adapt: frontend-slidesのCSS変数パターンを採用、ダーク・ミニマルに特化 |
| HTMLテンプレート（ツールバー+コンテンツ+JS） | references/html-template.md | Adapt: frontend-slidesのテンプレート構造をドキュメント用に再設計 |
| contenteditable + sessionStorage | references/html-template.md | Adapt: localStorage→sessionStorage |
| 画像ペースト処理 | references/html-template.md | As-is |
| Blob→ダウンロード処理 | references/html-template.md | As-is |
| 編集ON/OFFトグル | references/html-template.md | 新規UI設計（明示的ボタン） |
