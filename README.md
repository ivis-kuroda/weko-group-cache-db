# weko-group-cache-db / グループ情報キャッシュ機能
<!-- Pytest Coverage Comment:Begin -->
<a href="https://github.com/ivis-kuroda/weko-group-cache-db/blob/main/README.md"><img alt="Coverage" src="https://img.shields.io/badge/Coverage-100%25-brightgreen.svg" /></a>
<!-- Pytest Coverage Comment:End -->

## 概要
指定された機関のグループ情報を学認クラウドゲートウェイサービスのGroups APIから取得し、Redisにキャッシュを作成する。  
キャッシュは機関単位で作成され、Redisのキーは以下の構造化したハッシュ型で保存される。
グループ情報はグループIDをカンマ区切りで連結した文字列として保存される。

| キー                                | バリュー   |
| ----------------------------------- | ---------- |
| `xxx_repo_nii_ac_jp_gakunin_groups` | `updated_at` ：`"2025-11-14T04:27:28+00:00"` <br />`groups` ：`"jc_roles_sysadm,jc_xxx_repo_nii_ac_jp_roles_repoadm,jc_xxx_repo_nii_ac_jp_roles_contributor,jc_xxx_repo_nii_ac_jp_roles_comadm"` |
| `yyy_repo_nii_ac_jp_gakunin_groups` | `updated_at` ：`"2025-11-14T04:29:12+00:00"` <br />`groups` ：… |


## 環境構築

### 必要要件
* DockerfileよりDockerイメージをビルドできる環境
* mAP Core APIへ接続できるネットワーク環境
*	JAIRO Cloudが使用するRedisへ接続できるネットワーク環境

### Dockerイメージ
[Dockerfile](./Dockerfile)を使用してDockerイメージをビルドすることで、環境構築および実行が可能。  
デフォルトの動作では、コンテナの起動直後に、`/var/mnt`ディレクトリにマウントされた機関のSSL証明書・SSL鍵ファイルと、  
`/var/repositories.txt` にマウントされたFQDNリストファイルを使用して、全機関のグループ情報を取得し、Redisにキャッシュを作成する。

```
# デフォルトの起動時コマンド
CMD ["sh", "-c", "COLUMNS=120 exec wgcd run -d /var/mnt -l /var/repositories.txt"]
```

後述する実行方法に従ってコマンドをオーバーライドすれば、既定の動作を変更することが可能。


## 実行方法

### コマンドラインインターフェース概要
コマンドラインインターフェースは `wgcd` コマンドで実行する。

```
$ wgcd --help

  Usage: wgcd [OPTIONS] COMMAND [ARGS]...

  Run the command line interface for weko-group-cache-db.

  Options
  ────────────────────────────────────────────────────────────────────────────────────────────  
  --help   Show this message and exit.


  Commands
  ────────────────────────────────────────────────────────────────────────────────────────────  
  one      Fetch and cache groups for a single institution.
  run      Fetch and cache groups for all institutions.
```


### 全体実行
設定された機関すべてに対してグループ情報を取得し、機関単位でRedisにキャッシュを作成する。  
マウントされたディレクトリからFQDNリストファイルとSSL証明書・SSL鍵ファイルを使用して実行するディレクトリベースの実行方法と、機関情報を記述したTOMLファイルを使用して実行するファイルベースの実行方法がある。

#### ヘルプ表示

```
$ wgcd run --help

  Usage: wgcd run [OPTIONS]

  Fetch and cache groups for all institutions.
  Cannot specify both --file-path and --directory-path/--fqdn-list-file.

  Options
  ───────────────────────────────────────────────────────────────────────────────────────────────────────  
  -f   --file-path        FILE        Specify the path to the TOML file containing institution data.
  -d   --directory-path   DIRECTORY   Specify the path to the directory containing institution TLS files.
  -l   --fqdn-list-file   FILE        Specify the path to the file containing FQDN list.
  -c   --config-path      FILE        Specify the path to the configuration TOML file.
                                      [default=config.toml]
       --help                         Show this message and exit. 
```

#### オプション

| オプション名     | 短縮形 | 説明                                                                              |
| ---------------- | :----: | --------------------------------------------------------------------------------- |
| --file-path      | -f     | 機関情報TOMLファイルのパスを指定                                                  |
| --directory-path | -d     | 機関のSSL証明書・SSL鍵ファイルが格納されたフォルダの存在するディレクトリを指定    |
| --fqdn-list-file | -l     | 機関のFQDNが記載されたファイルのパスを指定                                        |
| --config-path    | -c     | コマンド実行時に参照する設定用TOMLファイルのパスを指定（デフォルト：config.toml） |

* ディレクトリベースの実行をする場合、`--directory-path`と`--fqdn-list-file`を両方指定する。
* ファイルベースの実行をする場合、`--file-path`を指定する。
* `--file-path`と`--directory-path`/`--fqdn-list-file`は同時に指定することができない。


### 単体実行
1つの機関に接続しているグループ情報を取得し、キャッシュDBへ登録する。  
マウントされたディレクトリからFQDNリストファイルとSSL証明書・SSL鍵ファイルを使用して実行するディレクトリベースの実行方法と、機関情報を記述したTOMLファイルを使用して実行するファイルベースの実行方法がある。

### ヘルプ表示

```
$ wgcd one --help
  Usage: wgcd one [OPTIONS] FQDN

  Fetch and cache groups for a single institution.
  Cannot specify both --file-path and --directory-path/--fqdn-list-file.

  Arguments
  ───────────────────────────────────────────────────────────────────────────────────────────────────────  
  FQDN   TEXT   [required] Specify the FQDN of the institution to fetch and cache groups for.


  Options
  ───────────────────────────────────────────────────────────────────────────────────────────────────────  
  -f   --file-path        FILE        Specify the path to the TOML file containing institution data.
  -d   --directory-path   DIRECTORY   Specify the path to the directory containing institution TLS files.
  -l   --fqdn-list-file   FILE        Specify the path to the file containing FQDN list.
  -c   --config-path      FILE        Specify the path to the configuration TOML file.
                                      [default=config.toml]
       --help                         Show this message and exit.
```

#### 引数
| 名称 | 必須 | 説明                                                                       |
| ---- | :--: | -------------------------------------------------------------------------- |
| FQDN |  ○  | グループ情報を取得し、キャッシュDBに登録する機関のFQDN（ドメイン名）を指定 |

#### オプション
| オプション名     | 短縮形 | 説明                                                                              |
| ---------------- | :----: | --------------------------------------------------------------------------------- |
| --file-path      | -f     | 機関情報TOMLファイルのパスを指定                                                  |
| --directory-path | -d     | 機関のSSL証明書・SSL鍵ファイルが格納されたフォルダの存在するディレクトリを指定    |
| --fqdn-list-file | -l     | 機関のFQDNが記載されたファイルのパスを指定                                        |
| --config-path    | -c     | コマンド実行時に参照する設定用TOMLファイルのパスを指定（デフォルト：config.toml） |

* ディレクトリベースの実行をする場合、`--directory-path`と`--fqdn-list-file`を両方指定する。
* ファイルベースの実行をする場合、`--file-path`を指定する。
* `--file-path`と`--directory-path`/`--fqdn-list-file`は同時に指定することができない。


## 各種設定
### TLSファイル構成要件
ディレクトリベースの実行をする場合に必要なTLSファイルの構成要件について説明する。

* `--directory-path` に指定するディレクトリは、である場合は以下の構造である必要がある。例えば、FQDNが sample.repo.nii.ac.jp である機関のSSL証明書・SSL鍵ファイルを使用する場合、

  ```
  /var/mnt
  ├── sample.repo.nii.ac.jp
  │   ├── server.crt
  │   └── server.key
  └── another.repo.nii.ac.jp
      ├── server.crt
      └── server.key
  ```

* 機関のSSL証明書ファイル名は`server.crt`、SSL鍵ファイル名は`server.key`でなければならない。
* 後述のFQDNリストファイルに記載されたFQDNに対応するディレクトリが存在しない場合、その機関のグループ情報は取得されない。  
  また、このファイルに記載されていないFQDNに対応するディレクトリが存在しても、その機関のグループ情報は取得されない。

### FQDNリストファイル
ディレクトリベースの実行をする場合に必要なFQDNリストファイルの記載方法について説明する。

* FQDNリストファイルには、機関のFQDNを1行ごとに記載する。スペース区切りの記述をパースして先頭のFQDNを使用する。
* `#` で始まる行はコメント行として扱われ、無視される。
* 空行は無視される。

  ```
  #<WEKO2_FQDN> <WEKO3_FQDN> ...
  sample.repo.nii.ac.jp sample.repo.nii.ac.jp
  another.repo.nii.ac.jp another.repo.nii.ac.jp
  # test.repo.nii.ac.jp test.repo.nii.ac.jp
  ...
  ```

* FQDNリストファイルに記載されたFQDNに対応するディレクトリが`--directory-path`に指定されたディレクトリ内に存在しない場合、またはTLSファイルが存在しない場合、その機関のグループ情報は取得されない。
* このファイルに記載されていないFQDNに対応するディレクトリが存在しても、その機関のグループ情報は取得されない。


### 機関情報TOMLファイル
ファイルベースの実行をする場合に必要な機関情報TOMLファイルの記載方法について説明する。

* 1機関ごとに `[[institutions]]` テーブルを作成し、キーと値のペアで各種情報を記載する。

  ```
  [[institutions]]
  name = "Sample University"
  fqdn = "sample.repo.nii.ac.jp"
  spid = "jc_sample_rcos_nii_ac_jp"
  cert = "certs/sample.crt"
  key = "certs/sample.key"
  ```

* それぞれのキーは以下の通り定義する。

  | 変数名 | 必須 | 説明                                            |
  | ------ | :--: | ----------------------------------------------- |
  | name   |      | 機関名                                          |
  | fqdn   |  ○  | 機関のFQDN（ドメイン名）                        |
  | spid   |  ○  | 機関の学認クラウドゲートウェイでのSPコネクタID  |
  | cert   |  ○  | 機関のSSL証明書ファイルのパス                   |
  | key    |  ○  | 機関のSSL鍵ファイルのパス                       |


### カスタム設定値
[config.toml](./config.toml)に設定値を記載することで、実行時に設定値を反映して実行することが可能。  
また、環境変数、`.env`ファイル、Kubernetesのシークレットマウントによっても設定値を反映することが可能。

`MAP_GROUPS_API_ENDPOINT`以外はデフォルトの設定値があるため、それ以外は必要に応じて上書きしたい設定値のみを記載すればよい。  
`config.toml`に記述する場合、大文字小文字は区別されない.

| 設定名                  | 型     | デフォルト値    | 説明                                                                                     |
| ----------------------- | ------ | --------------- | ---------------------------------------------------------------------------------------- |
| DEVELOPMENT             | 真偽値 | False           | 開発環境フラグ                                                                           |
| LOG_LEVEL               | 文字列 | INFO            | ログレベル<br>"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"のうちから指定              |
| SP_CONNECTOR_ID_PREFIX  | 文字列 | jc_             | SPコネクタIDのプレフィックス                                                             |
| CACHE_KEY_SUFFIX        | 文字列 | _gakunin_groups | Redisに登録するグループ情報のキーのサフィックス                                          |
| CACHE_TTL               | 数値   | 86400           | Redisに登録するグループ情報のキャッシュ有効期間（秒）<br>0未満が指定されると無期限となる |
| MAP_GROUPS_API_ENDPOINT | 文字列 | -               | 学認クラウドゲートウェイサービスのGroups APIのエンドポイント                             |
| REQUEST_TIMEOUT         | 数値   | 20              | Groups APIへ接続した際のタイムアウト時間（秒）                                           |
| REQUEST_INTERVAL        | 数値   | 3               | Groups APIからグループ情報を取得する際のリクエスト間隔（秒）                             |
| REQUEST_RETRIES         | 数値   | 3               | グループ情報取得・キャッシュDBへの登録処理のリトライ回数                                 |
| REQUEST_RETRY_BASE      | 数値   | 4               | グループ情報取得・キャッシュDBへの登録処理のリトライ時の指数バックオフの基準時間（秒）   |
| REQUEST_RETRY_FACTOR    | 数値   | 5               | グループ情報取得・キャッシュDBへの登録処理のリトライ時の指数バックオフの係数（秒）       |
| REQUEST_RETRY_MAX       | 数値   | 90              | グループ情報取得・キャッシュDBへの登録処理のリトライ時の指数バックオフの最大時間（秒）   |
| REDIS_TYPE              | 文字列 | redis           | 使用するRedisの種類<br>"redis", "sentinel"のうちから指定                                 |
| REDIS_HOST              | 文字列 | localhost       | Redisのホスト名                                                                          |
| REDIS_PORT              | 数値   | 6379            | Redisのポート番号                                                                        |
| REDIS_DB_INDEX          | 数値   | 4               | グループ情報を格納するRedisのDBインデックス                                              |
| REDIS_SENTINEL_MASTER   | 文字列 | None            | Redis Sentinelマスターのサーバー名                                                       |
| SENTINELS               | -      | None            | Redis Sentinelの設定一覧                                                                 |
| SENTINELS.host          | 文字列 |                 | Redis Sentinelのホスト名                                                                 |
| SENTINELS.port          | 数値   |                 | Redis Sentinelのポート番号                                                               |

※ Redis Sentinel の設定値をTOMLファイルに記載する場合の例
```
[[sentinels]]
host = "sendinel-1"
port = 26379

[[sentinels]]
host = "sendinel-2"
port = 26378

[[sentinels]]
host = "sendinel-3"
port = 26377
```

設定値の優先順位は以下の通り。

1. TOMLファイル
2. 環境変数
3. `.env`ファイル
4. Kubernetesのシークレットマウント
5. デフォルト値（`MAP_GROUPS_API_ENDPOINT`以外）

## 開発環境構築

VScodeを使用する場合、Dev Containers機能を使用してワンクリックで開発環境を構築できる。

### 手動インストール
パッケージ管理には [uv](https://github.com/astral-sh/uv) を使用している。

```
$ git clone https://github.com/RCOSDP/weko-group-cache-db.git && cd weko-group-cache-db
$ pip install uv && \
  uv sync --frozen && \
  uv pip install .
```

### CI
以下のタスクが [pyproject.toml](./pyproject.toml) の [tool.taskipy.tasks] セクションに定義されている。  
仮想環境がアクティブな状態で、`task <タスク名>` コマンドで実行できる。  

```
$ task -l
test          pytest
test:cov      pytest --cov=weko_group_cache_db --cov-branch --cov-report=term --cov-report=html
lint          uvx ruff check
lint:fix      uvx ruff check --fix
format        uvx ruff format
typecheck     pyright
check-updates uvx --from=pip-check-updates pcu pyproject.toml
```

GitHub ActionsでCIが実行される。
* test:cov: テストカバレッジの計測とレポートの生成
* lint: コードの静的解析
* typecheck: 型チェック
