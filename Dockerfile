FROM python:3.13-slim

WORKDIR /app

# システム依存パッケージのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Poetry のインストール
RUN pip install --no-cache-dir poetry

# 依存関係ファイルをコピー
COPY pyproject.toml poetry.lock* ./

# 依存関係のインストール（仮想環境を作成せずにシステムにインストール）
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# アプリケーションコードをコピー
COPY src/ ./src/

# 出力ディレクトリを作成
RUN mkdir -p src/outputs

# 作業ディレクトリを src に設定
WORKDIR /app/src

# 実行コマンド
CMD ["python", "main.py"]
