# Celery Task Test Application

FlaskとCeleryを使用した非同期タスク処理のテストアプリケーションです。

## 必要な環境

- Python 3.11以上
- MongoDB (ポート27017)
- Redis (ポート6379)

## セットアップ

1. 依存パッケージのインストール:
```sh
pip install -r requirements.txt
```

2. MongoDBとRedisの起動を確認

## 実行方法

### Celeryワーカーの起動

```sh
celery -A task:task_app worker --loglevel=info
```

### Flaskサーバーの起動

```sh
python server.py
```

サーバーは http://localhost:8888 で起動します。

## API エンドポイント

- `GET /` - ヘルスチェック
- `GET /task` - ZIPファイル作成タスクを開始
- `GET /task/<task_id>` - タスクのステータス確認
- `GET /task/<task_id>?operation=download` - 完了したタスクの結果(ZIPファイル)をダウンロード

## 設定

[.env](.env)ファイルで以下の設定が可能です:

- `CELERY_TASK_RESULT_EXPIRES` - タスク結果の有効期限(秒)

## 仕組み

1. `/task`エンドポイントにアクセスすると、[`make_file`](task.py)タスクが非同期で実行されます
2. タスクは30秒間スリープした後、3つのテキストファイルを含むZIPファイルを生成します
3. タスクIDを使用してステータスを確認し、完了後にダウンロードできます