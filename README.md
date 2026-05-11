# Capital Quest Corporation, Ltd. — 公式HP

独立系M&Aアドバイザリー Capital Quest Corporation, Ltd. のコーポレートサイト。  
静的 HTML/CSS/JS で構成、GitHub Pages 上で配信。

- **ライブURL**：https://yumiba924-a11y.github.io/CQCHP/
- **リポジトリ**：https://github.com/yumiba924-a11y/CQCHP
- **ホスティング**：GitHub Pages（`main` ブランチ自動デプロイ、1–2分で反映）

---

## ファイル構成

```
/
├── index.html             ← JP HOME
├── about.html             ← JP 会社情報
├── services.html          ← JP 事業内容
├── track-record.html      ← JP 過去実績
├── team.html              ← JP チーム
├── en/                    ← EN（英語版、5ページ同構造）
│   ├── index.html
│   └── ...
├── cn/                    ← CN（簡体字版、5ページ同構造）
│   ├── index.html
│   └── ...
├── assets/
│   ├── css/style.css      ← 全ページ共有スタイル（~4100行）
│   ├── js/site.js         ← 全ページ共有JS（ハンバーガー、スクロールreveal）
│   ├── img/               ← 写真・ロゴ・地図画像
│   │   ├── hero/          ← ヒーロー動画用ポスター画像
│   │   ├── team/          ← 経営陣・メンバー写真
│   │   ├── group/         ← グループ会社ロゴ
│   │   └── track-record/  ← 案件ロゴ
│   ├── video/             ← ヒーロー動画（TK/NY2/HK2/VN.mp4）
│   └── logo/cqc/          ← CQCブランドロゴ
└── README.md              ← このファイル
```

**ページ数**：15ファイル（5ページ × 3言語）

---

## 開発・編集ワークフロー

### 1. ローカル編集
- HTMLは普通のテキストエディタで直接編集
- CSSは `assets/css/style.css` 単一ファイル
- JSはページ内インライン（HOMEのヒーロー）または `assets/js/site.js`

### 2. 動作確認
- **必ず GitHub Pages のライブURLで確認**（`file://` は相対パス問題で正しくない）
- 反映は push 後 1–2分

### 3. コミット & プッシュ
```bash
git add -A
git commit -m "変更内容"
git push origin main
```

### 4. キャッシュバスター
- CSS / JS 変更時は **全15HTMLファイルのキャッシュバスター を一括更新**
- 形式：`style.css?v=20260511q` / `site.js?v=20260511q`
- 命名規則：`YYYYMMDD<英字>`（同日複数リリース時は a→b→c... と繰り上げ）
- 一括更新 PowerShell：
  ```powershell
  $dirs = @('.', './en', './cn')
  foreach ($d in $dirs) {
    Get-ChildItem -Path $d -Filter '*.html' -File | ForEach-Object {
      $c = Get-Content -Raw $_.FullName -Encoding UTF8
      $c = $c -replace 'style\.css\?v=20260511q', 'style.css?v=20260511r'
      [System.IO.File]::WriteAllText($_.FullName, $c, (New-Object System.Text.UTF8Encoding $false))
    }
  }
  ```

---

## 多言語の整合性ルール（重要）

### 翻訳ポリシー
| 用語 | JP | EN | CN |
|---|---|---|---|
| 社名 | キャピタル・クエスト株式会社 | Capital Quest Corporation, Ltd. | Capital Quest Corporation, Ltd. |
| 投資銀行 | 投資銀行 | Investment Banking | 投资银行 |
| M&A | M&A | M&A | M&A（英語そのまま） |
| 人名 | 筒井 豊春 | Toyoharu Tsutsui | 筒井 豊春（漢字そのまま） |
| GAP | Global Alliance Partners | Global Alliance Partners | Global Alliance Partners |

### 同期ルール
- **内容変更（テキスト/構造）は必ず JP/EN/CN 3言語すべてに反映**
- 1言語だけ更新するのはNG（齟齬が生まれる）

### ナビゲーション項目（CN は最近統一済）
| JP | EN | CN |
|---|---|---|
| ホーム | Home | 主页 |
| 会社情報 | About | 公司信息 |
| 事業内容 | Services | 业务领域 |
| 過去実績 | Track Record | 业绩记录 |
| チーム | Team | 团队 |

---

## 主要コンポーネントマップ

### ヒーロー（HOME のみ）
- **動画**：TK→NY→HK→VN を 8.5秒ごとにクロスフェード（2秒遷移）
- **テロップ**：左下に大型JP/小型EN、シーンごとに差し替え
- **都市インジケーター**：右上にドット4個＋現在の都市名
- **操作ボタン**（PCのみ）：前/一時停止/次
- **VN テーマ**：VN シーンのみテロップを**白帯+墨文字**に切替（夜景視認性確保）
- 実装：`index.html` 末尾のインライン `<script>`

### 過去実績カード
- 構造：`.tx-card`
  ```
  ┌─────────────────────────┐
  │ 北米｜クロスボーダー     │ ← 緑薄背景バンド（edge-to-edge）
  ├─────────────────────────┤
  │   [ロゴA] | [ロゴB]       │ ← 中央配置（コンテナ高140px統一）
  │   会社A × 会社B          │ ← タイトル中央揃え
  │   ─────                  │ ← ゴールド罫線中央
  │   説明文（左揃え）        │
  │   Advisor to: ○○         │
  └─────────────────────────┘
  ```
- HOME：自動スクロールカルーセル（16枚、マーキー無限ループ）
- track-record.html：5地域タブで切替（合計20枚）

### スクロールリビール
- **すべてのページ**で IntersectionObserver により自動適用
- 対象セレクタ：`.section-header` `.chairman__pull` `.pillar-card` `.person-card` 等（`site.js` 参照）
- 動き：30px 上スライド + フェード、0.7s ease
- 同一セクション内は 0.1s ずつ stagger（最大4要素）
- **写真は除外**（`.chairman__photo` `.president__photo`）
- `prefers-reduced-motion: reduce` で完全無効化

---

## ブランド・コンプライアンス

### ブランド
- **社名**：Capital Quest Corporation, Ltd. （略称 CQC）
- **ブランドカラー**：深緑 `#00492C` (RGB 0, 73, 44) — CSS変数 `--c-forest`
- **ゴールドアクセント**：CSS変数 `--c-gold`
- **ロゴ**：獅子 + CQC + イタリック社名（`assets/logo/cqc/cqc-logo-transparent.png`）

### グループ関係（重要）
- **CQC は CFH（Capital Financial Holdings）グループの子会社**
- **GAP（Global Alliance Partners）は CFH グループ会社 ではない**
  - GAP は国際 M&A 連携ネットワーク（独立組織）
  - 「Group」見出しの下に GAP を置かない
  - 構造図で CFH 傘下に GAP を描かない
  - 別カラム・別段落で明確に分離

### コンプライアンス基本ルール
- ❌ 進行中案件の金額・件数（営業秘密）
- ✅ 公知の過去実績のみ
- ❌ 「最大級」「No.1」等の主観表現（景表法リスク）
- ❌ 「機関投資家向け運用アドバイザリー」等、金商法上の投資助言業に該当しうる文言
- ✅ 「クロスボーダーM&Aアドバイザリー」等の事実ベース表現

### 人物表記（重要）
- **筒井 豊春**（代表取締役会長）
  - CQC は登記上の代表取締役
  - GAP は「**共同創設メンバー・日本代表**」（取締役表記NG）
  - CS First Boston は「**現UBS**」を必ず付ける（CS→Credit Suisse→UBS lineage）
- **庄司 俊之, CFA**（社長執行役員）
  - **「代表取締役社長」NG**（登記上の代表取締役は筒井のみ）
  - 社長執行役員 / Toshiyuki Shoji, CFA で統一

---

## CSS 設計メモ

### 設計思想
- OS フォント前提（ウェブフォント未使用、軽量重視）
- ブランドカラー・スペーシングは CSS変数で集約（`:root` ブロック）
- BEM風命名（`.block__element--modifier`）

### CSS変数の主要トークン
- 色：`--c-bg`, `--c-ink`, `--c-forest`, `--c-gold`, `--c-paper` 等
- フォント：`--font-mincho`, `--font-gothic`, `--font-sans-en`
- サイズ：`--fs-display`, `--fs-title`, `--fs-body`, `--fs-caption`
- 間隔：`--space-section`, `--space-block`, `--space-element`

### ブレイクポイント
- PC：`@media (min-width: 1025px)`
- タブレット/モバイル：`@media (max-width: 1024px)`
- スマホ小：`@media (max-width: 768px)`
- 極小：`@media (max-width: 480px)`

---

## 既知の特殊対応

| 箇所 | 内容 |
|---|---|
| BridgePoint ロゴ | 他ロゴと異なり140px高、ロゴコンテナも140pxで統一 |
| FUNAI ロゴ | 白ロゴのため `filter: invert(1)` で黒に反転 |
| VN シーンテロップ | 夜景背景のため白帯+墨文字（`.is-light` クラス） |
| GAP セクション | グループ会社一覧とは完全分離 |
| Windows reduce-motion 対策 | ヒーローサイクルは常時実行（OS設定に依存しない）|

---

## トラブルシューティング

### 動画が動かない
- `prefers-reduced-motion` ではなく、ブラウザ自体のautoplay制限が疑わしい
- 必ず `muted` 属性付き（autoplay+muted=モバイルでもOK）
- iOS Safari でのみ起きる場合は `playsinline` 確認

### CSS変更が反映されない
- キャッシュバスター更新を忘れていないか確認
- ブラウザの強制リロード（Ctrl+F5 / Cmd+Shift+R）
- GitHub Pages の反映待ち（push後最大2分）

### 多言語ページ間で表示が違う
- 内容変更は3言語同期が原則。1言語のみの更新は禁止。
- ナビゲーション項目名・人物肩書・住所表記は特に注意

---

## 連絡先

サイト責任者：弓場 彰吾（投資調査部 課長）
