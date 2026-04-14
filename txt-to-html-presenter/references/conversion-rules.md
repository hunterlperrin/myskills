# Conversion Rules

## Format Detection

### Priority: Extension first, content fallback

```
1. .md  → Markdown
2. .csv → CSV
3. .txt → Plain text
4. Other → Content analysis:
   - Lines starting with # and containing ** or - lists → Markdown
   - Lines with consistent comma separation → CSV
   - Default → Plain text
```

## Markdown → HTML

Convert these elements in order. Use semantic HTML tags.

| Markdown | HTML | Notes |
|----------|------|-------|
| `# Heading` | `<h1>` | `##` → `<h2>`, etc. up to `<h6>` |
| `**bold**` | `<strong>` | |
| `*italic*` | `<em>` | |
| `~~strike~~` | `<del>` | |
| `` `code` `` | `<code>` | Inline only |
| ```` ```lang ```` | `<pre><code>` | Wrap in `<pre>`. Add language as comment if present |
| `- item` or `* item` | `<ul><li>` | Nested lists by indentation |
| `1. item` | `<ol><li>` | |
| `> quote` | `<blockquote>` | Nested by `>>` |
| `[text](url)` | `<a href="url">text</a>` | `target="_blank"` for external links |
| `![alt](url)` | `<img src="url" alt="alt">` | |
| `---` or `***` | `<hr>` | |
| `| col | col |` | `<table>` | Wrap in `<div class="table-container">` |
| Blank line | Paragraph break | Wrap text blocks in `<p>` |

### Markdown table handling

```
| Header 1 | Header 2 |    →    <div class="table-container">
|----------|----------|          <table>
| Cell 1   | Cell 2   |           <thead><tr><th>Header 1</th><th>Header 2</th></tr></thead>
                                   <tbody><tr><td>Cell 1</td><td>Cell 2</td></tr></tbody>
                                 </table>
                               </div>
```

The separator row (`|---|---|`) determines alignment:
- `:---` → left (default)
- `:---:` → center
- `---:` → right

## CSV → HTML

### Rules

1. **First row = header**: Always treat the first row as `<thead>`
2. **Delimiter detection**: Try comma first. If a row has more tabs than commas, use tab. If semicolons, use semicolons
3. **Quoted fields**: Handle `"field with, comma"` correctly — don't split inside quotes
4. **Empty cells**: Render as empty `<td></td>`
5. **Wrap in table-container**: Always use `<div class="table-container"><table>...</table></div>`

### Structure

```html
<div class="table-container">
  <table>
    <thead>
      <tr><th>Col1</th><th>Col2</th><th>Col3</th></tr>
    </thead>
    <tbody>
      <tr><td>val1</td><td>val2</td><td>val3</td></tr>
      <!-- ... -->
    </tbody>
  </table>
</div>
```

### Large CSV handling

If the CSV has more than 100 rows, add a note above the table:
```html
<p style="color: var(--text-muted); font-size: var(--font-size-sm);">Showing all N rows</p>
```

## Plain Text → HTML

### Rules

1. **Paragraph splitting**: Split on blank lines (two or more consecutive newlines). Each block becomes `<p>`
2. **Single newlines**: Preserve as `<br>` within a paragraph
3. **Indented blocks**: Lines starting with 4+ spaces or a tab → treat as `<pre><code>`
4. **URL detection**: Auto-link URLs matching `https?://[^\s]+` → `<a href="url" target="_blank">url</a>`
5. **Title inference**: If the first line is short (≤80 chars) and followed by a blank line, treat it as `<h1>`

## Multiple Files

When converting multiple files into a single HTML:

1. Use the first filename as the document title and output filename
2. Insert a section divider between each file's content:
   ```html
   <hr style="margin: var(--space-2xl) 0; border-color: var(--border-primary);">
   <h2>filename.ext</h2>
   ```
3. Each file is independently parsed by its format rules
