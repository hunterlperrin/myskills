# myskills

Claude Code のカスタムスキル集。別PCへの移植用リポジトリ。

## セットアップ

```bash
# クローンしてシンボリックリンクを張る
git clone https://github.com/hunterlperrin/myskills.git ~/myskills
ln -s ~/myskills/* ~/.claude/skills/
```

## スキル一覧

| スキル | 説明 |
|--------|------|
| find-repo | GitHubリポジトリを検索してREADMEを評価 |
| find-skill | タスクに合った公開スキルを探す |
| investigate | コードベースや技術的問題を体系的に調査 |
| review-changes | git diffの変更内容をレビュー |
| skill-architect | カスタムスキルの設計・構築 |
| txt-to-html-presenter | テキストファイルをHTML化 |
