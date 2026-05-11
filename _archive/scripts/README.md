# CSS監査・整理用スクリプト

2026-05-11 のローンチ前クリーンアップで使用したワンオフ Python スクリプト。
将来 CSS の肥大化や重複に気づいた時の参考として保管。

## 各スクリプト

| ファイル | 役割 |
|---|---|
| `_audit_css.py` | HTML/JS で使われていない CSS クラスを検出して style.css から削除 |
| `_audit_vars.py` | 未使用の CSS 変数と @keyframes を検出 |
| `_remove_unused.py` | _audit_vars.py で見つかった未使用変数・キーフレームを削除 |
| `_audit_dupes.py` | 同じセレクタが複数回定義されていないかチェック |
| `_compact_blanks.py` | 連続する空行を圧縮 |

## 使い方

リポジトリ直下で：
```bash
python3 _archive/scripts/_audit_css.py
python3 _archive/scripts/_audit_vars.py
python3 _archive/scripts/_audit_dupes.py
```

⚠️ 注意：これらは「ベストエフォート」のスクリプトで、誤検出の可能性あり。
削除前に必ず差分を確認すること。
