# Market Survey: txt-to-html-presenter

## 軸1: 直接競合

| Discovery | Type | Importance | Summary |
|-----------|------|------------|---------|
| frontend-slides (zarazhangrui) | skill | ★★★ | テキスト/PPTXからアニメーション付きHTMLプレゼン生成。12デザインプリセット、ゼロ依存単一HTML、localStorage編集機能あり |
| HTML Presentation Generator (mcpmarket) | skill | ★★☆ | 企業グレードのスライドHTML生成。16:9固定、12カラムグリッド、プロカラーパレット |
| Markdown To HTML (claudeskills.info) | skill | ★☆☆ | MD→HTML基本変換。スタイリング・インタラクティブ機能なし |

**直接該当するスキルは存在しない**: txt/md/csvを「画面共有向け編集可能ドキュメント」に変換するスキルは未発見。frontend-slidesは最も近いが「スライド」特化であり「ドキュメント」ではない。

## 軸2: 品質評価ツール

| Discovery | Type | Importance | Summary |
|-----------|------|------------|---------|
| agentskills.io validator (skills-ref) | tool | ★★☆ | `skills-ref validate ./skill` でフロントマター検証 |
| skill-architect内蔵QAスクリプト | tool | ★★★ | validate_skill.py + qa_checklist.py |

## 軸3: 公式仕様・ガイド

| Discovery | Type | Importance | Summary |
|-----------|------|------------|---------|
| agentskills.io/specification | spec | ★★★ | SKILL.md ≤500行、name: lowercase+hyphens ≤64chars、description ≤1024chars、Progressive Disclosure 3層構造 |
| Anthropic skill-creator | guide | ★★☆ | 公式スキル作成メタスキル。正しい構造のテンプレート |

## 軸4: エコシステム・配布

| Discovery | Type | Importance | Summary |
|-----------|------|------------|---------|
| anthropics/skills | platform | ★★☆ | 公式スキルリポジトリ。web-artifacts-builder, pptx等 |
| awesome-agent-skills (VoltAgent) | platform | ★☆☆ | 1000+スキルのキュレーションリスト |
| mcpmarket.com | platform | ★☆☆ | スキル・MCPマーケットプレイス |

## 軸5: 隣接ドメイン

| Discovery | Type | Importance | Summary |
|-----------|------|------------|---------|
| web-artifacts-builder (Anthropic公式) | skill | ★★☆ | React+Tailwind+shadcn/uiでの複雑HTMLアーティファクト構築。我々の用途にはオーバースペック |
| claude-office-skills (tfriedel) | skill | ★☆☆ | PPTX/DOCX/XLSX生成群。HTML→PPTX変換含む |

---

## 差分分析（★★★: frontend-slides）

| Feature | Our approach | frontend-slides | 採用？ |
|---------|-------------|-----------------|--------|
| 用途 | ドキュメント表示（画面共有） | スライドプレゼン | No — スライドではなくドキュメント形式 |
| 入力形式 | txt/md/csv等の自動判定 | テキスト or PPTX | Adapt — 複数形式対応の構造解析を独自実装 |
| デザイン | ダーク・ミニマル固定 | 12プリセットから選択 | No — ユーザー要件はダーク・ミニマル一択 |
| 編集機能 | sessionStorage + contenteditable | localStorage + contenteditable | Adapt — sessionStorageに変更（セッション終了で自動削除） |
| 画像対応 | クリップボードペースト(Base64) | 事前提供画像の埋め込み | No — リアルタイムペーストは独自要件 |
| ダウンロード | DOM→Blob→ダウンロード | なし（ファイルは生成時に出力） | No — 独自実装 |
| ゼロ依存単一HTML | Yes | Yes | Yes — そのまま採用 |
| 編集ON/OFF | 明示的トグルボタン | ホバー/キーボード | Adapt — より明示的なUIに |
| "AI slop"回避 | ミニマルデザイン指針 | 詳細なデザイン哲学 | Yes — anti-generic原則を採用 |

## 主要知見

1. **単一HTML・ゼロ依存**はこの分野のスタンダード。必須要件として確定
2. **contenteditable + Storage**は検証済みパターン。frontend-slidesがlocalStorage版を実装済み → sessionStorageへの変更は容易
3. **構造解析（md/csv/txt判定）**は既存スキルにない独自価値。ここが差別化ポイント
4. **画像ペースト**も既存スキルにない独自機能
5. agentskills.io specの制約: SKILL.md ≤500行、詳細はreferences/に分離
