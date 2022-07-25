# CS-NewPointPlus-Container

## ローカル環境

### 開発環境準備(Docker)

#### 初期設定
初期設定時、以下の手順で初期設定を行う。

1. `.env.example` を複製し、 `.env` をrepositoryのrootDirに作成する
2. `.env` の値を必要に応じて変更する（APIキーの値など）
3. `make init` コマンドを実行時、各ディレクトリに必要なファイル・ディレクトリを作成する
4. `make build` コマンドを実行しDocker環境を構築する

`.env.example` は `.env` のテンプレート用でGit管理されるため、直接APIキーなどGit管理すべきでない値は記述せず、必ず `.env` を複製した上で `.env` に記述・使用すること。

`.env.example` に変更があった場合、1〜3を再度行うこと。

また、 `Dockerfile` に変更があった場合、 `make reubild` コマンドを実行し、Docker環境を再構築すること。

### 開発環境アクセス

#### 実行方法

|コマンド|処理内容|
|---|---|
|`make build`|dockerのビルド|
|`make rebuild`|dockerをキャッシュを無視してビルド|
|`make up`|docker環境の起動|
|`make down`|docker環境の停止|

#### dockerアクセス

```
# Django
docker exec -it cs-newpointplus-container_django_1 bash

# frontend
docker exec -it cs-newpointplus-container_frontend_1 bash

# mysql
docker exec -it cs-newpointplus-container_mysql_1 bash
```

#### 各Webページアクセス
各Webページ

|Web名|URL|対応プロジェクト|
|---|---|---|
|管理コンソール|[console.localhost](http://console.localhost/#/)|`web-console`|
|店舗Web|[shop.localhost](http://shop.localhost/#/)|`web-shop`|
|マイページ|[mypage.localhost](http://mypage.localhost/#/)|`web-mypage`|
|残高照会ページ|[card.localhost](http://card.localhost/#/)|`web-card`|

#### APIアクセス

http://<サービス名>.localhost/<サービス名>/api/<バージョン>
(例: http://shop.localhost/shop/api/v1 )



## 各コンテナについて

### Django

#### 新規アプリケーション立ち上げ
Djangoコンテナ内にて以下コマンドを実行する

```
$ python manage.py startapp xxx(アプリ名)
```

#### Open API出力について
Djangoコンテナ内にて以下コマンドを実行する

```
bash open_api_generater.sh
```

#### migrationについて
開発においてDBのテーブルを変更する必要があった場合はmodels配下のクラスを修正後
python manage.py makemigrations
を実施すること
カラムの追加削除以外の処理が必要な場合は適宜生成されたmigrationファイルに修正をすること

#### ディレクトリ構成

```
/─django          # Djangoディレクトリ
   ├─batch        # Batch機能群
   ├─config       # 設定ファイル群
   ├─database     # Modelおよびmigrationファイル群
   ├─open_api     # API仕様書作成用ファイル群
   ├─utils        # Utilityファイル群
   ├─v1_admin     # 管理コンソール用API機能群
   ├─v1_card      # 残高照会ページ用API機能群
   └─v1_shop      # 店舗端末用API機能群
```

### frontend

#### frontendホットリロード
docker環境を立ち上げた後、以下のコマンドにてホットリロード可能

```
# コンテナにアクセス
docker exec -it cs-newpointplus-container_frontend_1 bash

# node_modulesがからの場合
yarn install

# ホットリロード
yarn workspace <ホットリロードしたいプロジェクトのpackage.jsonのname> watch
```

#### i18n対応
フロントエンドに関しては、 [vue-i18n](https://kazupon.github.io/vue-i18n/) にて対応する。

言語ファイルに関しては以下の手順で生成・配置する。

1. [テキスト一覧シート](https://docs.google.com/spreadsheets/d/1LGMd5dOpWqsDlPz888FYwYd1i59CGG5akU6Gz5yrk4A) に画面に出力するテキストを追記する
2. スクリプトを実行し、言語ファイルを出力する
3. [出力された言語ファイル](https://drive.google.com/drive/folders/1MBR6ZM_kWJGCqC3g6VVSbJ8KtRMOUadg) （ `*.json` ）を各Webごとに `frontend/packages/web-*/src/locales` に配置する

テキスト一覧シートに関しては、 [使い方](https://docs.google.com/spreadsheets/d/1LGMd5dOpWqsDlPz888FYwYd1i59CGG5akU6Gz5yrk4A/edit#gid=1540693616) を参照。

#### ディレクトリ構成

```
/┬─django           # Djangoディレクトリ
 └─frontend         # フロントエンドルートディレクトリ
   └─packages
     ├─api          # API
     ├─utils        # Utility系
     ├─web-console    # 管理コンソール
     ├─web-card     # 残高照会ページ
     ├─web-mypage # マイページ
     └─web-shop     # 店舗Web
```
