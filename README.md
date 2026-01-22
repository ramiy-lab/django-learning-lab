# django-learning-lab

Django を基礎から実務レベルまで体系的に学習するための **学習ログ兼実験用リポジトリ** です。
単なる写経ではなく、

* 「なぜそうなるのか」
* 「どこまで ORM を使い、どこから SQL を意識するのか」
* 「実務ではどう判断するのか」

を言語化しながら段階的に理解を深めることを目的としています。

---

## 🎯 このリポジトリの目的

* Django の **内部構造と思想** を理解する
* ORM を「魔法」ではなく **道具として使える状態**になる
* 後続の

  * Django REST Framework
  * AWS デプロイ
  * 実務設計
    につながる **土台を固める**

---

## 🧭 学習方針

* **1リポジトリで一貫して学習を継続**
* 学習途中のコード・試行錯誤も履歴として残す
* 架空のサンプルではなく、**実際に動かしたコードのみを記録**
* ORM / SQL / 設計判断を常に意識する

---

## 🚀 Django 学習ロードマップ（全体像）

### ① Django 基礎環境と基礎構造

* プロジェクト作成
* ディレクトリ構造の理解
* `settings.py` / `urls.py` / `views.py` の役割

---

### ② URL → View → Template（MVT の基礎）

* URL 設計
* 関数ベースビュー（FBV）
* Template と context
* extends / block / static

---

### ③ Model（ORM）とデータベース

* Model クラス設計
* Migration の思想
* Query / QuerySet の正体
* 遅延評価と評価タイミング
* CRUD 操作（get / filter / update / delete）
* ORM と SQL の境界判断
* N+1 問題の理解

👉 **現在このフェーズを学習中**

---

### ④ Form・バリデーション・POST 処理

* Django Form / ModelForm
* CSRF
* バリデーション設計
* エラー表示と再レンダリング

---

### ⑤ 認証・認可（Auth）

* Django Auth の構造
* ログイン / ログアウト
* User モデル拡張
* 権限管理

---

### ⑥ Class-Based Views（CBV）

* ListView / DetailView
* Create / Update / Delete
* Mixin の役割
* 実務での使い分け

---

### ⑦ Django REST Framework（DRF）

* Serializer
* ViewSet / Router
* 認証・認可
* API 設計

---

### ⑧ 非同期処理・タスク

* Celery
* Redis
* バックグラウンド処理

---

### ⑨ デプロイ（AWS）

* EC2 / RDS / S3
* Nginx / Gunicorn
* 本番設定
* 環境変数管理

---

### ⑩ 実務レベル設計

* settings 分割
* サービス層設計
* テスト（pytest）
* ログ設計
* CI/CD

---

## 📂 このリポジトリの位置づけ

* ポートフォリオではない
* 完成品を目指す場所でもない
* **思考と理解のログを残す場所**

👉 「学習の過程」そのものを価値として残す。

---

## 📝 補足

* コードは学習フェーズに応じて変化します
* 一部リファクタや削除も意図的に行います
* すべては **理解を深めるため**

---

## 📌 最後に

このリポジトリは
**Django を「使えるようになる」ための思考ログ**です。

完成よりも、
理解・判断・設計の積み重ねを重視しています。


とかやりたくなったら、そこも一緒に整えよう。
