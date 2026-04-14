# Design System: Dark Minimal

## CSS Variables

```css
:root {
  /* Colors */
  --bg-primary: #0d1117;
  --bg-secondary: #161b22;
  --bg-tertiary: #21262d;
  --bg-toolbar: #010409;
  --text-primary: #e6edf3;
  --text-secondary: #8b949e;
  --text-muted: #484f58;
  --border-primary: #30363d;
  --border-secondary: #21262d;
  --accent: #58a6ff;
  --accent-hover: #79c0ff;
  --success: #3fb950;
  --warning: #d29922;
  --danger: #f85149;
  --code-bg: #161b22;
  --table-stripe: #161b22;

  /* Typography */
  --font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  --font-mono: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  --font-size-base: 16px;
  --font-size-sm: 14px;
  --font-size-lg: 18px;
  --font-size-h1: 32px;
  --font-size-h2: 24px;
  --font-size-h3: 20px;
  --line-height: 1.7;
  --line-height-tight: 1.3;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --content-max-width: 860px;

  /* Misc */
  --radius: 6px;
  --transition: 0.15s ease;
}
```

## Base Styles

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  font-size: var(--font-size-base);
  scroll-behavior: smooth;
}

body {
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: var(--font-body);
  line-height: var(--line-height);
  -webkit-font-smoothing: antialiased;
}
```

## Toolbar

Fixed at top. Contains edit toggle (left) and download button (right). Height: 48px.

```css
.toolbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 48px;
  background: var(--bg-toolbar);
  border-bottom: 1px solid var(--border-primary);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-lg);
  z-index: 1000;
  user-select: none;
}

.toolbar-btn {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  border: 1px solid var(--border-primary);
  padding: var(--space-xs) var(--space-md);
  border-radius: var(--radius);
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: all var(--transition);
  font-family: var(--font-body);
}

.toolbar-btn:hover {
  background: var(--border-primary);
  color: var(--text-primary);
}

.toolbar-btn.active {
  background: var(--accent);
  color: #ffffff;
  border-color: var(--accent);
}
```

## Content Area

Centered, max-width constrained, padding-top for toolbar clearance.

```css
.content {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: calc(48px + var(--space-2xl)) var(--space-lg) var(--space-2xl);
  min-height: 100vh;
}

.content:focus {
  outline: none;
}

.content[contenteditable="true"] {
  border-left: 2px solid var(--accent);
  padding-left: calc(var(--space-lg) - 2px);
}
```

## Typography

```css
h1, h2, h3, h4, h5, h6 {
  color: var(--text-primary);
  line-height: var(--line-height-tight);
  margin-top: var(--space-2xl);
  margin-bottom: var(--space-md);
  font-weight: 600;
}

h1 { font-size: var(--font-size-h1); border-bottom: 1px solid var(--border-primary); padding-bottom: var(--space-sm); }
h2 { font-size: var(--font-size-h2); }
h3 { font-size: var(--font-size-h3); }

p { margin-bottom: var(--space-md); }

a { color: var(--accent); text-decoration: none; }
a:hover { color: var(--accent-hover); text-decoration: underline; }

strong { font-weight: 600; color: var(--text-primary); }
em { font-style: italic; color: var(--text-secondary); }
```

## Code

```css
code {
  background: var(--code-bg);
  color: var(--accent);
  padding: 2px 6px;
  border-radius: 3px;
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
}

pre {
  background: var(--code-bg);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius);
  padding: var(--space-md);
  overflow-x: auto;
  margin-bottom: var(--space-md);
}

pre code {
  background: none;
  padding: 0;
  color: var(--text-primary);
}
```

## Tables

```css
.table-container {
  overflow-x: auto;
  margin-bottom: var(--space-md);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius);
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--font-size-sm);
}

th {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  font-weight: 600;
  text-align: left;
  padding: var(--space-sm) var(--space-md);
  border-bottom: 2px solid var(--border-primary);
}

td {
  padding: var(--space-sm) var(--space-md);
  border-bottom: 1px solid var(--border-secondary);
}

tr:nth-child(even) td {
  background: var(--table-stripe);
}
```

## Lists

```css
ul, ol {
  margin-bottom: var(--space-md);
  padding-left: var(--space-lg);
}

li {
  margin-bottom: var(--space-xs);
}

li > ul, li > ol {
  margin-top: var(--space-xs);
  margin-bottom: 0;
}
```

## Blockquotes

```css
blockquote {
  border-left: 3px solid var(--accent);
  padding: var(--space-sm) var(--space-md);
  margin-bottom: var(--space-md);
  color: var(--text-secondary);
  background: var(--bg-secondary);
  border-radius: 0 var(--radius) var(--radius) 0;
}
```

## Images (pasted)

```css
.content img {
  max-width: 100%;
  height: auto;
  border-radius: var(--radius);
  margin: var(--space-md) 0;
  border: 1px solid var(--border-primary);
}
```

## Edit Mode Indicator

```css
.edit-indicator {
  display: none;
  position: fixed;
  bottom: var(--space-md);
  right: var(--space-md);
  background: var(--accent);
  color: #ffffff;
  padding: var(--space-xs) var(--space-md);
  border-radius: var(--radius);
  font-size: var(--font-size-sm);
  z-index: 1000;
}

.edit-indicator.visible {
  display: block;
}
```

## Design Rules

1. **No external fonts** — System font stack only. Reliable, fast, no network dependency
2. **No gradients** — Flat solid colors only
3. **No animations** — Transitions limited to hover states (0.15s ease)
4. **No shadows** — Borders for separation, not box-shadow
5. **Muted accent** — Blue (#58a6ff) used sparingly: links, active states, edit indicator
6. **Generous whitespace** — line-height 1.7, content max-width 860px
