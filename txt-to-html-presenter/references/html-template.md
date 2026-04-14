# HTML Template

Complete HTML skeleton. Include ALL sections in every generated file. Replace `{{TITLE}}` and `{{CONTENT}}` with actual values.

## Template

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{TITLE}}</title>
  <style>
    /* === PASTE ALL CSS FROM design-system.md HERE === */
  </style>
</head>
<body>

  <!-- === TOOLBAR === -->
  <div class="toolbar">
    <div class="toolbar-left">
      <button class="toolbar-btn" id="editToggle" onclick="toggleEdit()">Edit: OFF</button>
    </div>
    <div class="toolbar-right">
      <button class="toolbar-btn" id="downloadBtn" onclick="downloadHTML()">Download</button>
    </div>
  </div>

  <!-- === CONTENT === -->
  <div class="content" id="content">
    {{CONTENT}}
  </div>

  <!-- === EDIT INDICATOR === -->
  <div class="edit-indicator" id="editIndicator">Editing</div>

  <!-- === JAVASCRIPT === -->
  <script>
    // --- State ---
    let isEditing = false;
    const STORAGE_KEY = 'txt-to-html-presenter-' + document.title;

    // --- Edit Toggle ---
    function toggleEdit() {
      isEditing = !isEditing;
      const content = document.getElementById('content');
      const btn = document.getElementById('editToggle');
      const indicator = document.getElementById('editIndicator');

      content.contentEditable = isEditing;
      btn.textContent = 'Edit: ' + (isEditing ? 'ON' : 'OFF');
      btn.classList.toggle('active', isEditing);
      indicator.classList.toggle('visible', isEditing);

      if (isEditing) {
        content.focus();
      } else {
        saveToStorage();
      }
    }

    // --- sessionStorage Auto-save ---
    let saveTimer = null;

    function saveToStorage() {
      const content = document.getElementById('content');
      try {
        sessionStorage.setItem(STORAGE_KEY, content.innerHTML);
      } catch (e) {
        // sessionStorage full or unavailable — silently ignore
      }
    }

    function loadFromStorage() {
      try {
        const saved = sessionStorage.getItem(STORAGE_KEY);
        if (saved) {
          document.getElementById('content').innerHTML = saved;
        }
      } catch (e) {
        // sessionStorage unavailable — use original content
      }
    }

    function debounceSave() {
      clearTimeout(saveTimer);
      saveTimer = setTimeout(saveToStorage, 500);
    }

    // --- Download ---
    function downloadHTML() {
      // Temporarily disable editing for clean output
      const content = document.getElementById('content');
      const wasEditing = isEditing;
      if (wasEditing) {
        content.contentEditable = false;
      }

      const html = document.documentElement.outerHTML;
      const blob = new Blob(['<!DOCTYPE html>\n' + html], { type: 'text/html; charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = document.title + '.html';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      // Restore editing state
      if (wasEditing) {
        content.contentEditable = true;
      }
    }

    // --- Clipboard Image Paste ---
    document.getElementById('content').addEventListener('paste', function(e) {
      if (!isEditing) return;

      const items = e.clipboardData && e.clipboardData.items;
      if (!items) return;

      for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
          e.preventDefault();
          const file = items[i].getAsFile();
          const reader = new FileReader();
          reader.onload = function(event) {
            const img = document.createElement('img');
            img.src = event.target.result;
            const selection = window.getSelection();
            if (selection.rangeCount > 0) {
              const range = selection.getRangeAt(0);
              range.deleteContents();
              range.insertNode(img);
              range.setStartAfter(img);
              range.collapse(true);
              selection.removeAllRanges();
              selection.addRange(range);
            } else {
              document.getElementById('content').appendChild(img);
            }
            debounceSave();
          };
          reader.readAsDataURL(file);
          break;
        }
      }
    });

    // --- Input Event for Auto-save ---
    document.getElementById('content').addEventListener('input', debounceSave);

    // --- Restore on Load ---
    window.addEventListener('DOMContentLoaded', loadFromStorage);
  </script>

</body>
</html>
```

## Implementation Notes

1. **STORAGE_KEY**: Uses document title for uniqueness. Multiple converted files can coexist in the same session without overwriting each other
2. **sessionStorage vs localStorage**: sessionStorage auto-clears when the tab closes. No manual cleanup needed. This is intentional — edits are temporary for the session
3. **Download captures current state**: The download function serializes the entire DOM including edits and pasted images. The downloaded file is fully self-contained
4. **Image paste**: Only works when editing is ON. Images are Base64-encoded and inserted at cursor position
5. **Debounce**: 500ms delay prevents excessive storage writes during rapid typing
6. **Error handling**: Storage operations are wrapped in try/catch. If sessionStorage is full or unavailable (private browsing), the document still works — just without save/restore
