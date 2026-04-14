# Satellite Control System

Satellite telemetry and command management web application.
Built with Python / Django as a learning project.

衛星へのコマンド送信・テレメトリデータ受信を管理するWebアプリケーションです。
Python（Django）のプロジェクトとして作成しました。

---

## このプロジェクトでできること

- 衛星の基本情報を登録・編集・削除する
- 衛星にコマンドを送信する（フォーム入力）
- 衛星からのテレメトリデータ（温度・電圧など）を一覧表示する
- DjangoのCRUD操作（作成・読取・更新・削除）を学べる

---

## 使用技術

| 技術 | 役割 |
|------|------|
| Python 3.12 | プログラミング言語 |
| Django 5.1.4 | Webアプリのフレームワーク（骨組み） |
| Docker | コンテナ環境（どのPCでも同じ環境で動かせる） |
| SQLite | データベース（データの保存先） |
| Bootstrap 5 | 画面デザイン用フレームワーク |
| gunicorn | 本番用Webサーバー |
| whitenoise | CSS・画像などの静的ファイル配信 |

---

## パッケージの役割（requirements.txt）

### Django==5.1.4
Webアプリを作るためのフレームワーク（骨組み）です。
家を建てるための「建築キット」のようなものです。
画面表示、データベース操作、URL管理などが全部入っています。

### gunicorn==21.2.0
本番環境でDjangoアプリを動かすための「Webサーバー」です。
お店の「受付係」のようなもので、ユーザーのリクエストを受け取ってDjangoに渡します。
Djangoに付属の開発サーバーは練習用なので、本番ではgunicornを使います。

### whitenoise==6.8.2
CSS・画像などの「静的ファイル」を配信するためのツールです。
お店の「見た目の装飾担当」のようなもので、デザインや画像をブラウザに届けます。

### リクエストの流れ

    ユーザー（ブラウザ）
        ↓ リクエスト
    gunicorn（受付係）
        ↓
    Django（本体）→ 画面・データ処理
        ↓
    whitenoise → CSS・画像を配信
        ↓ レスポンス
    ユーザー（画面が表示される）

---

## フォルダ構成

    C:\dev\satellite-control-system\
    |-- docker-compose.yml       # コンテナの管理設定（マンションの管理人）
    |-- Dockerfile               # コンテナの設計図（部屋の準備手順書）
    |-- requirements.txt         # 使用パッケージ一覧（買い物リスト）
    |-- manage.py                # Django管理コマンド
    |-- db.sqlite3               # データベースファイル
    |-- config/                  # プロジェクト設定（マンション全体の管理規約）
    |   |-- __init__.py
    |   |-- settings.py          # メイン設定ファイル
    |   |-- urls.py              # ルートURL定義
    |   |-- asgi.py
    |   |-- wsgi.py
    |-- satellite/               # メインアプリ（衛星管制のお店）
    |   |-- migrations/          # マイグレーションファイル
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- apps.py
    |   |-- models.py            # データベースのテーブル定義
    |   |-- tests.py
    |   |-- views.py
    |-- static/
    |   |-- css/
    |       |-- style.css

---

## 重要な用語の解説

### Dockerに関する用語

| 用語 | 意味 | たとえ |
|------|------|--------|
| Docker | アプリの実行環境をまるごとパッケージにする技術 | 引っ越し先でもすぐ動く「持ち運べる部屋」 |
| Dockerfile | コンテナの設計図 | 部屋の準備手順書 |
| docker-compose.yml | 複数コンテナをまとめて管理する設定ファイル | マンションの管理人 |
| コンテナ | アプリが動く隔離された環境 | マンションの1室 |
| イメージ | コンテナの元になるテンプレート | 部屋の設計図から作った模型 |

### Djangoに関する用語

| 用語 | 意味 | たとえ |
|------|------|--------|
| プロジェクト（config） | アプリ全体の設定 | マンション全体の管理 |
| アプリ（satellite） | プロジェクト内の1つの機能単位 | マンション内の1つのお店 |
| モデル（Model） | データベースのテーブル定義 | Excelの列見出し |
| マイグレーション | モデルの内容をデータベースに反映する作業 | 設計メモから実際にExcelファイルを作る作業 |
| ビュー（View） | 画面に何を表示するかのロジック | お店の接客マニュアル |
| テンプレート（Template） | HTMLの画面デザイン | お店の内装デザイン |
| URL | どのアドレスでどの画面を表示するかの定義 | お店の住所と案内板 |
| ForeignKey | テーブル同士をつなぐ仕組み | 「この注文はどのお客さんのもの？」 |
| CharField | 短い文字列のフィールド | 名前・IDなどに使う |
| FloatField | 小数点の数字フィールド | 温度・電圧などに使う |
| DateTimeField | 日時のフィールド | いつ送信した？に使う |
| auto_now_add=True | データ作成時に自動で現在日時を入れる | 自動タイムスタンプ |

---

## データベース設計（models.py）

### Satellite（衛星テーブル）
衛星の基本情報を管理します。

| カラム名 | データ型 | 説明 | 例 |
|---------|---------|------|-----|
| name | CharField | 衛星名 | ALOS-4 |
| satellite_id | CharField（一意） | 衛星の識別ID | SAT-001 |
| orbit_type | CharField | 軌道種別 | LEO |
| status | 選択肢 | 運用状態 | Active / Standby |
| launched_at | DateTimeField | 打上げ日時 | 2025-01-15 10:00 |

### Command（コマンドテーブル）
衛星へ送信するコマンドを管理します。

| カラム名 | データ型 | 説明 | 例 |
|---------|---------|------|-----|
| satellite | ForeignKey | 対象衛星（衛星テーブルと連携） | ALOS-4 |
| command_type | 選択肢 | コマンド種別 | Attitude Control |
| command_code | CharField | コマンドコード | CMD-ATT-001 |
| parameters | TextField | パラメータ | angle=45.0 |
| status | 選択肢 | ステータス | Pending / Sent |
| operator | CharField | オペレータ名 | Tanaka |

### TelemetryData（テレメトリテーブル）
衛星から受信するデータを管理します。

| カラム名 | データ型 | 説明 | 例 |
|---------|---------|------|-----|
| satellite | ForeignKey | 衛星（衛星テーブルと連携） | ALOS-4 |
| temperature_battery | FloatField | バッテリー温度 | 25.3 C |
| temperature_solar_panel | FloatField | 太陽電池パネル温度 | 45.0 C |
| voltage_bus | FloatField | バス電圧 | 28.5 V |
| current_bus | FloatField | バス電流 | 2.1 A |
| power_generation | FloatField | 発電量 | 60.0 W |
| health_status | 選択肢 | 健全性ステータス | Nominal / Warning / Critical |

---

## 環境構築の手順

### 前提条件
- Python がインストールされていること
- Docker Desktop がインストールされ、起動していること
- Cursor（エディタ）がインストールされていること

### Step 1: プロジェクトフォルダの作成

    mkdir C:\dev\satellite-control-system
    cd C:\dev\satellite-control-system

Cursorで「Open project」から上記フォルダを開きます。

### Step 2: requirements.txt の作成
使用するPythonパッケージの一覧を定義します。

    New-Item -Path "requirements.txt" -ItemType File

ファイルを開いて以下を入力して保存（Ctrl + S）：

    Django==5.1.4
    gunicorn==21.2.0
    whitenoise==6.8.2

### Step 3: Dockerfile の作成
コンテナの設計図を作ります。
日本語コメントは文字化けの原因になるため、英語のみで記述します。

    @"
    FROM python:3.12-slim
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --upgrade pip && pip install -r requirements.txt
    COPY . .
    EXPOSE 8000
    CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
    "@ | Out-File -FilePath Dockerfile -Encoding utf8

#### Dockerfileの各行の意味

| 行 | やっていること | たとえ |
|----|--------------|--------|
| FROM python:3.12-slim | Python入りの部屋を借りる | 家具付き物件を選ぶ |
| ENV ... | 部屋のルールを設定 | 「靴は脱ぐ」的なルール |
| WORKDIR /app | 作業場所を決める | 「この机で作業する」 |
| COPY requirements.txt . | 買い物リストを持ち込む | メモを部屋に置く |
| RUN pip install ... | パッケージをインストール | 買い物リストの物を購入 |
| COPY . . | 全ファイルを持ち込む | 荷物を全部搬入 |
| EXPOSE 8000 | 8000番ポートを開ける | 玄関のドアを開ける |
| CMD [...] | サーバーを起動 | お店をオープンする |

### Step 4: docker-compose.yml の作成
コンテナをまとめて管理する設定ファイルを作ります。

    @"
    services:
      web:
        build: .
        container_name: satellite-control
        ports:
          - "8000:8000"
        volumes:
          - .:/app
        environment:
          - DEBUG=1
          - DJANGO_SETTINGS_MODULE=config.settings
        command: python manage.py runserver 0.0.0.0:8000
    "@ | Out-File -FilePath docker-compose.yml -Encoding utf8

#### docker-compose.ymlの各行の意味

| 行 | 意味 | たとえ |
|----|------|--------|
| build: . | 今のフォルダのDockerfileを使う | この設計図で部屋を作って |
| container_name | コンテナに名前をつける | 部屋に表札をつける |
| ports: "8000:8000" | PCの8000番とコンテナの8000番をつなぐ | 玄関同士をつなぐ通路 |
| volumes: .:/app | PCのファイルとコンテナを同期 | 共有フォルダ |
| environment | 環境変数を設定 | 部屋のルール設定 |
| command | 起動時に実行するコマンド | 入室したらまずこれをやる |

### Step 5: Dockerイメージをビルド

    docker-compose build

初回は2〜3分かかります。Docker Desktopが起動していないとエラーになります。

### Step 6: Djangoプロジェクトを生成
Djangoの設定ファイル一式を自動で作ります。（マンション全体の骨組み）

    docker-compose run --rm web django-admin startproject config .

末尾の .（ドット）を忘れないこと！現在のフォルダにプロジェクトを作る意味です。

### Step 7: Djangoアプリを生成
衛星管制の機能を持つアプリを作ります。（マンション内のお店）

    docker-compose run --rm web python manage.py startapp satellite

### Step 8: settings.py の編集
config/settings.py を開いて、全内容を設定ファイルに置き換えます。
主な設定内容：
- INSTALLED_APPS に satellite を追加（アプリの登録）
- MIDDLEWARE に whitenoise を追加（静的ファイル配信）
- LANGUAGE_CODE = "ja"（日本語化）
- TIME_ZONE = "Asia/Tokyo"（日本時間）
- DATABASES でSQLiteを指定

### Step 9: 静的ファイル用フォルダの作成

    mkdir static\css
    New-Item -Path "static\css\style.css" -ItemType File -Force

### Step 10: models.py の編集
satellite/models.py にデータベースのテーブル定義を記述します。
- Satellite（衛星情報）
- Command（コマンド情報）
- TelemetryData（テレメトリデータ）

### Step 11: マイグレーション（データベース作成）
models.pyの内容をデータベースに反映します。

    docker-compose run --rm web python manage.py makemigrations
    docker-compose run --rm web python manage.py migrate

#### マイグレーションの流れ

    models.py（設計図）
        ↓ makemigrations
    マイグレーションファイル（指示書）
        ↓ migrate
    データベース（実際のテーブル完成！）

---

## トラブルシューティング

### ターミナルで日本語が文字化けする

    chcp 65001

ターミナルの文字コードをUTF-8に変更するコマンドです。
Dockerfileには日本語を書かないのがベストです。

### Cursorで「インポートを解決できませんでした」と警告が出る
DjangoはDockerコンテナ内にインストールされているため、
Cursor（ローカルPC）からは見えないだけです。実行には問題ありません。

    Cursor（PC）     → Djangoが無い → 警告を出す
    Docker（コンテナ）→ Djangoがある → 正常に動く

### docker-composeで「version is obsolete」と警告が出る
docker-compose.yml の version: "3.9" の行を削除してください。
最新のDocker Composeではバージョン指定は不要になりました。

---

## Dockerコマンド一覧

| コマンド | 意味 | たとえ |
|---------|------|--------|
| docker-compose build | コンテナイメージを作成 | 部屋を建てる |
| docker-compose run --rm web ... | 一時的にコンテナを起動してコマンド実行 | 部屋に入って1つ作業して出る |
| docker-compose up | アプリケーションを起動 | お店をオープン |
| docker-compose down | アプリケーションを停止 | お店を閉める |

## Djangoコマンド一覧

| コマンド | 意味 | たとえ |
|---------|------|--------|
| django-admin startproject config . | プロジェクト骨組みを生成 | マンション全体を建てる |
| python manage.py startapp satellite | アプリを生成 | お店を新設する |
| python manage.py makemigrations | マイグレーションファイルを作成 | DB変更の指示書を作る |
| python manage.py migrate | マイグレーションを実行 | 指示書をDBに反映する |

## Gitコマンド一覧

| コマンド | 意味 | たとえ |
|---------|------|--------|
| git init | このフォルダでGit管理を開始 | ノートを新しく用意する |
| git add . | 全ファイルを記録対象にする | 今日やった作業を全部メモする準備 |
| git commit -m "..." | 変更を記録する | メモに日付とタイトルをつけて保存 |
| git push | GitHubにアップロードする | 本棚のノートを最新版に差し替え |

---

## 今後の予定（TODO）

- [ ] forms.py の作成（入力フォーム）
- [ ] views.py の作成（画面ロジック・CRUD操作）
- [ ] URL定義の作成（satellite/urls.py）
- [ ] HTMLテンプレートの作成（ダッシュボード・コマンド・テレメトリ画面）
- [ ] admin.py の設定（Django管理画面）
- [ ] サンプルデータの投入
- [ ] 本番URLへデプロイ

---

## .gitignore について

### .gitignore とは？
Gitで管理しなくてよいファイルを指定するリストです。
たとえるなら、「引っ越しの時に持っていかない物リスト」です。
データベースファイルやキャッシュなど、共有不要なものを除外します。

### 除外しているファイルと理由

| 除外対象 | 何のファイル？ | 除外する理由 |
|---------|-------------|-------------|
| __pycache__/ | Pythonの自動生成キャッシュ | 他の人には不要。各自の環境で自動生成される |
| *.py[cod] | Pythonのコンパイル済みファイル | 自動生成されるので共有不要 |
| db.sqlite3 | データベースファイル | 各自の環境でマイグレーションして作り直せる |
| staticfiles/ | 本番用の静的ファイル | コマンドで自動生成できる |
| *.log | ログファイル | 各自の環境で出力されるもの |
| .env | 環境変数ファイル | パスワードなどの機密情報が入る可能性がある |
| .cursor/ | Cursorエディタの個人設定 | 他の人のエディタ設定には不要 |
| .vscode/ | VSCodeの個人設定 | 同上 |
| Thumbs.db | Windowsの自動生成ファイル | OS固有のファイルで共有不要 |
| .DS_Store | Macの自動生成ファイル | OS固有のファイルで共有不要 |

### .gitignore の作成コマンド

    @"
    # Python
    __pycache__/
    *.py[cod]
    *.egg-info/
    .eggs/
    # Django
    db.sqlite3
    staticfiles/
    *.log
    # Docker
    .docker/
    # Environment
    .env
    *.env
    # IDE
    .vscode/
    .cursor/
    *.swp
    *.swo
    # OS
    .DS_Store
    Thumbs.db
    "@ | Out-File -FilePath .gitignore -Encoding utf8

### ポイント
- .gitignore はプロジェクトの一番最初に作るのがベスト
- 機密情報（パスワード・APIキーなど）は絶対にGitに含めない
- 自動生成されるファイルは基本的に除外する

---

## Day 2 で追加した内容

### forms.py（入力フォーム）

ユーザーが画面で入力するフォームの定義です。
たとえるなら、「申請書のテンプレート」です。
どの項目を入力させるか、どんな入力欄にするかを決めます。

3つのフォームを作成しました：

| フォーム名 | 用途 | たとえ |
|-----------|------|--------|
| SatelliteForm | 衛星の登録・編集画面 | 衛星の登録申請書 |
| CommandForm | コマンド送信画面 | コマンドの指示書 |
| TelemetryDataForm | テレメトリ手動入力画面 | データの記録用紙 |

#### forms.py の重要な用語

| 用語 | 意味 | たとえ |
|------|------|--------|
| ModelForm | モデル（テーブル）に基づいた自動フォーム | テーブルの列をそのまま入力欄にする |
| fields | フォームに表示する項目のリスト | 申請書に載せる項目を選ぶ |
| widgets | 入力欄の見た目を指定 | テキスト欄？プルダウン？数字欄？ |
| form-control | Bootstrapのデザインクラス | 入力欄をきれいに表示する |
| placeholder | 入力欄のヒント文字 | 薄いグレーの「例：〇〇」の文字 |

---

### views.py（画面ロジック）

ユーザーが画面にアクセスしたとき「何を表示するか」を決めるロジックです。
たとえるなら、「お店の接客マニュアル」です。

ここでCRUD操作を全て実装しています：

| 操作 | 英語 | やること |
|------|------|---------|
| C | Create | 新しいデータを作成 |
| R | Read | データを表示（一覧・詳細） |
| U | Update | データを編集 |
| D | Delete | データを削除 |

#### ビューの基本パターン

    def 関数名(request):
        1. データを取得する
        2. テンプレート（HTML）にデータを渡す
        3. 画面を表示する

#### Create（作成）の流れ

    ユーザーがフォーム画面にアクセス（GET）
        → 空のフォームを表示
    ユーザーが入力して送信ボタンを押す（POST）
        → データを保存して一覧画面に戻る

#### views.py の重要な用語

| 用語 | 意味 | たとえ |
|------|------|--------|
| request | ユーザーからのリクエスト情報 | お客さんの注文内容 |
| request.method | GET（表示）かPOST（送信）か | 「見せて」か「注文します」か |
| render | テンプレートにデータを渡して画面を返す | 注文票を見て料理を出す |
| redirect | 別の画面に移動する | 「あちらのカウンターへどうぞ」 |
| get_object_or_404 | データを取得。無ければ404エラー | 在庫を確認。無ければ「品切れ」 |
| messages.success | 成功メッセージを表示 | 「ご注文ありがとうございます」の表示 |
| context | テンプレートに渡すデータの辞書 | 料理と一緒に渡すメニュー表 |
| form.is_valid() | 入力内容が正しいかチェック | 記入漏れがないか確認 |
| form.save() | データをデータベースに保存 | 注文票を厨房に渡す |
| select_related | 関連テーブルを一緒に取得（高速化） | 注文と一緒にお客さん情報も取る |
| pk | Primary Key（データの識別番号） | お客さん番号、注文番号 |

---

### urls.py（URL定義）

「どのURLにアクセスしたら、どの画面を表示するか」を定義するファイルです。
たとえるなら、「お店の案内板・フロアマップ」です。

2つのファイルで構成されています：

    config/urls.py      → 全体のURL（ビルの入口案内）
    satellite/urls.py   → アプリのURL（お店の中の案内）

#### URL一覧表

| URL | 画面 | CRUD |
|-----|------|------|
| / | ダッシュボード | Read |
| /satellites/ | 衛星一覧 | Read |
| /satellites/create/ | 衛星登録 | Create |
| /satellites/1/edit/ | 衛星編集（ID=1） | Update |
| /satellites/1/delete/ | 衛星削除（ID=1） | Delete |
| /commands/ | コマンド一覧 | Read |
| /commands/create/ | コマンド作成 | Create |
| /commands/1/ | コマンド詳細（ID=1） | Read |
| /commands/1/send/ | コマンド送信実行 | Update |
| /commands/1/edit/ | コマンド編集 | Update |
| /commands/1/delete/ | コマンド削除 | Delete |
| /telemetry/ | テレメトリ一覧 | Read |
| /telemetry/create/ | テレメトリ登録 | Create |
| /telemetry/1/ | テレメトリ詳細 | Read |
| /telemetry/1/delete/ | テレメトリ削除 | Delete |

#### urls.py の重要な用語

| 用語 | 意味 | たとえ |
|------|------|--------|
| path() | URLとビューを結びつける | 「この住所に来たらこの人が対応」 |
| name="..." | URLに名前をつける | 住所にニックネームをつける |
| int:pk | URLの中に数字（ID）を含める | 「注文番号3番のお客様」 |
| include() | 別のurls.pyを読み込む | 「詳しくはこちらを参照」 |
| app_name | アプリの名前空間 | 「satellite:command_list」のように使える |

---

### HTMLテンプレート（画面デザイン）

ユーザーに見せる「画面のデザイン」を定義するHTMLファイルです。
たとえるなら、「お店の内装デザイン」です。

以下の11ファイルを作成しました：

| ファイル | 用途 |
|---------|------|
| base.html | 共通レイアウト（全ページの枠組み） |
| dashboard.html | ダッシュボード（トップページ） |
| satellite_list.html | 衛星一覧 |
| satellite_form.html | 衛星登録・編集フォーム |
| satellite_confirm_delete.html | 削除確認画面（共通） |
| command_list.html | コマンド一覧 |
| command_form.html | コマンド送信フォーム |
| command_detail.html | コマンド詳細 |
| telemetry_list.html | テレメトリ一覧 |
| telemetry_form.html | テレメトリ登録フォーム |
| telemetry_detail.html | テレメトリ詳細 |

#### テンプレートの重要な用語

| 用語 | 意味 | たとえ |
|------|------|--------|
| {% extends "base.html" %} | 共通レイアウトを継承する | 「お店の外装はそのまま使う」 |
| {% block content %} | 差し替え可能なコンテンツ部分 | 陳列スペースに商品を並べる |
| {{ 変数名 }} | データを画面に表示する | 渡されたメモの内容を見せる |
| {% for item in list %} | データを繰り返し表示 | 一覧表の各行を1つずつ表示 |
| {% if ... %} | 条件分岐 | 「データがあれば表示、なければメッセージ」 |
| {% csrf_token %} | セキュリティ用トークン（フォームに必須） | 「本人確認の印鑑」 |
| {% url 'name' %} | URL名からアドレスを自動生成 | 案内板のリンク |
| {{ value|date:"Y-m-d" }} | データをフォーマットして表示 | 日時を見やすい形に変換 |

#### テレメトリ画面の色分けルール

| 条件 | 色 | 意味 |
|------|-----|------|
| バッテリー温度 > 40 C | 赤 | 危険 |
| バッテリー温度 > 30 C | 黄 | 注意 |
| バッテリー温度 <= 30 C | 緑 | 正常 |
| バス電圧 < 24 V | 赤 | 危険 |
| バス電圧 < 26 V | 黄 | 注意 |
| バス電圧 >= 26 V | 緑 | 正常 |

---

### admin.py（Django管理画面）

Djangoに標準搭載されている「管理画面」の設定ファイルです。
たとえるなら、「お店のバックヤード（裏方管理室）」です。
ブラウザからデータの追加・編集・削除ができます。

#### admin.py の重要な用語

| 用語 | 意味 | たとえ |
|------|------|--------|
| @admin.register(Model) | モデルを管理画面に登録 | 「この商品を管理対象にする」 |
| list_display | 一覧画面で表示する列 | 「一覧表にどの列を見せるか」 |
| list_filter | 絞り込みフィルターを表示 | 「ステータスで絞り込める」 |
| search_fields | 検索ボックスで検索できる項目 | 「名前やIDで検索できる」 |

#### 管理画面のアクセス方法

    URL: http://localhost:8000/admin/
    ユーザー名: admin
    パスワード: （createsuperuserで設定したもの）

---

### Day 2 の実行手順まとめ

    Step 1:  forms.py を作成（satellite/forms.py）
    Step 2:  views.py を編集（satellite/views.py）
    Step 3:  urls.py を作成（satellite/urls.py）
    Step 4:  config/urls.py を編集
    Step 5:  テンプレートフォルダを作成
    Step 6:  base.html を作成
    Step 7:  dashboard.html を作成
    Step 8:  satellite_list.html を作成
    Step 9:  satellite_form.html を作成
    Step 10: satellite_confirm_delete.html を作成
    Step 11: command_list.html を作成
    Step 12: command_form.html を作成
    Step 13: command_detail.html を作成
    Step 14: telemetry_list.html を作成
    Step 15: telemetry_form.html を作成
    Step 16: telemetry_detail.html を作成
    Step 17: admin.py を編集
    Step 18: createsuperuser でスーパーユーザー作成
    Step 19: docker-compose up でサーバー起動
    Step 20: ブラウザで動作確認

---

## 今後の予定（TODO）更新

- [x] forms.py の作成（入力フォーム）
- [x] views.py の作成（画面ロジック・CRUD操作）
- [x] URL定義の作成（satellite/urls.py）
- [x] HTMLテンプレートの作成（ダッシュボード・コマンド・テレメトリ画面）
- [x] admin.py の設定（Django管理画面）
- [ ] サンプルデータの投入
- [ ] 本番URLへデプロイ

---

## 作成者

宇宙関連の地上システム開発に向けた、Python（Django）プロジェクトです。