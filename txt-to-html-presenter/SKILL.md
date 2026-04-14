---
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
---

# txt-to-html-presenter

Convert text-based files into polished, editable HTML documents optimized for screen sharing. Single self-contained HTML with no external dependencies.

## Features

- **Dark minimal design** — Clean, readable, professional
- **Edit ON/OFF** — Toggle inline editing with a single button
- **Auto-save** — sessionStorage preserves edits during the session, auto-deletes on tab close
- **Image paste** — Paste images from clipboard directly into the document (Base64 inline)
- **Download** — Save the current state as a standalone HTML file to ~/Downloads

## Supported Formats

| Format | Detection | Conversion |
|--------|-----------|------------|
| Markdown (.md) | Extension or `#` headings, `- ` lists, ``` blocks | Headings, lists, code blocks, tables, links, emphasis |
| CSV (.csv) | Extension or comma-separated structure | Styled HTML table with header row |
| Plain text (.txt, other) | Fallback | Paragraphs split by blank lines |

## Workflow

### Step 1: Read Input

Read the file(s) specified by the user. Determine format by extension first, then by content analysis as fallback.

If multiple files are specified, process each and combine into a single HTML with section dividers.

### Step 2: Generate HTML

Read the following references and apply them:

- **`references/design-system.md`** — CSS variables, typography, toolbar, layout rules
- **`references/html-template.md`** — Complete HTML structure with all JS features
- **`references/conversion-rules.md`** — Format-specific conversion logic

Generate a single self-contained HTML file. All CSS and JS must be inline. No external resources.

**Critical rules:**
- Use the exact CSS variables and color values from design-system.md
- Include ALL JS features from html-template.md (edit toggle, sessionStorage, download, image paste)
- Follow conversion-rules.md for format-specific HTML structure
- The HTML must work offline — zero external dependencies

### Step 3: Output

1. Write the HTML file to the same directory as the input file, named `[original-name].html`
   - Multiple files: use the first filename as base
2. Open with `open [filename].html`
3. Tell the user:
   - File location
   - How to use: Edit button (top-right) to toggle editing, Download button to save, paste images while editing
   - sessionStorage note: edits persist while the tab is open, cleared when the tab closes

## Quick Example

```
User: 「このreport.txtをHTMLに変換して」

Step 1 → report.txt読み取り、.txt拡張子 → プレーンテキスト判定
Step 2 → デザイン仕様・テンプレート・変換ルール読み込み → ダーク・ミニマルHTML生成（編集/DL/画像ペースト機能付き）
Step 3 → report.html出力 → ブラウザで開く
```

## Prohibitions

- **No external dependencies** — No CDN, npm, Google Fonts, or any external URL
- **No localStorage** — sessionStorage only (auto-deletes on tab/browser close)
- **No auto-download** — Download only on explicit user button click
- **No excessive decoration** — No gradient backgrounds, animations, or heavy shadows
- **No input file modification** — Source files are read-only; output as separate .html

## Troubleshooting

### Characters display incorrectly (mojibake)
Ensure the HTML has `<meta charset="UTF-8">`. If the source file uses a different encoding, convert it first with `iconv`.

### Layout breaks on very wide tables (CSV)
The template includes `overflow-x: auto` on table containers. If the table is extremely wide, suggest the user split columns or rotate to landscape view.

### Images pasted but not visible after download
Images are embedded as Base64 data URIs. If the HTML file size is very large (>10MB), the browser may struggle. Suggest reducing image sizes before pasting.

### Edit mode doesn't activate
Verify JavaScript is enabled in the browser. The edit toggle requires JS to set `contenteditable` on the content area.

## References

Read these when generating HTML — not before:

- **`references/design-system.md`** — Read at Step 2. CSS variables, colors, typography, toolbar design, layout rules for dark minimal theme.
- **`references/html-template.md`** — Read at Step 2. Complete HTML skeleton with toolbar, content area, and all JS features (edit toggle, sessionStorage, download, image paste).
- **`references/conversion-rules.md`** — Read at Step 2. Format detection logic and conversion rules for Markdown, CSV, and plain text.
