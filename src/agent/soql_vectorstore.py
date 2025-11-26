"""
SOQLドキュメントのベクトルストア管理モジュール
PostgreSQLにベクトルと本文を保存
"""
import os
import numpy as np
import psycopg2
from psycopg2.extras import execute_values
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# パス設定
DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")
TEXT_FILE = os.path.join(DOCS_DIR, "salesforce_soql_document.txt")

# グローバルキャッシュ
_model = None
_db_conn = None


def _get_db_config():
    """DB接続設定を取得"""
    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
        "user": os.getenv("POSTGRES_USER", "vectordb"),
        "password": os.getenv("POSTGRES_PASSWORD", "vectordb123"),
        "database": os.getenv("POSTGRES_DB", "soql_vectors")
    }


def _get_model():
    """Embeddingモデルを取得（シングルトン）"""
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def _get_db():
    """DBコネクションを取得"""
    global _db_conn
    if _db_conn is None or _db_conn.closed:
        config = _get_db_config()
        _db_conn = psycopg2.connect(**config)
    return _db_conn


def init_vectorstore():
    """ベクトルストアを初期化（初回のみ実行）"""
    conn = _get_db()
    cursor = conn.cursor()

    # テーブル作成
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            embedding BYTEA NOT NULL
        )
    """)
    conn.commit()

    # データが既に存在するか確認
    cursor.execute("SELECT COUNT(*) FROM chunks")
    count = cursor.fetchone()[0]

    if count > 0:
        print(f"既存のベクトルDB をロードします（{count} チャンク）")
        return

    print("ベクトルストアを初期化中...")

    # テキスト読み込み
    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    print(f"ドキュメントサイズ: {len(text)} 文字")

    # チャンク分割（より大きなチャンクで文脈を保持）
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=400,
        length_function=len,
        separators=["\n\n", "\n", "。", "、", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    print(f"チャンク数: {len(chunks)}")

    # ベクトル化
    model = _get_model()
    print("ベクトル化中...")
    embeddings = model.encode(chunks, show_progress_bar=True)

    # データ挿入
    data = [
        (chunk, embedding.astype(np.float32).tobytes())
        for chunk, embedding in zip(chunks, embeddings)
    ]

    execute_values(
        cursor,
        "INSERT INTO chunks (content, embedding) VALUES %s",
        data,
        template="(%s, %s)"
    )

    conn.commit()
    print(f"ベクトルストアをPostgreSQLに保存しました")


def search_relevant_docs(query: str, k: int = 5) -> list[str]:
    """クエリに関連するドキュメントを検索"""
    # DB初期化確認
    init_vectorstore()

    model = _get_model()

    # クエリをベクトル化
    query_embedding = model.encode([query])[0]

    # DBから全チャンクを取得してコサイン類似度計算
    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT content, embedding FROM chunks")
    rows = cursor.fetchall()

    # 類似度計算
    similarities = []
    for content, embedding_bytes in rows:
        embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
        # コサイン類似度
        similarity = np.dot(query_embedding, embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
        )
        similarities.append((content, similarity))

    # 上位k件を返す
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [content for content, _ in similarities[:k]]


def rebuild_vectorstore():
    """ベクトルストアを再構築（ドキュメント更新時に使用）"""
    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS chunks")
    conn.commit()
    print("テーブルを削除しました")

    global _db_conn
    _db_conn = None

    init_vectorstore()


if __name__ == "__main__":
    print("ベクトルストアをテスト中...")

    # 初期化
    init_vectorstore()

    # 検索テスト
    test_queries = [
        "日付リテラル LAST_N_MONTHS 使い方",
        "WHERE句 NULL 比較",
        "リレーション __c __r 変換"
    ]

    for query in test_queries:
        print(f"\n--- クエリ: {query} ---")
        results = search_relevant_docs(query, k=3)
        for i, result in enumerate(results, 1):
            print(f"\n[結果 {i}]")
            print(result[:300] + "..." if len(result) > 300 else result)
