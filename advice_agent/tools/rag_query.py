"""
Vertex AI RAG corporaから関連情報を収集するツール
"""

from vertexai import rag
import vertexai
from google.adk.tools.tool_context import ToolContext

import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_RAG_CORPUS_NAME = os.environ.get("GOOGLE_RAG_CORPUS_NAME")


def search_support_policy_info(query: str, tool_context: ToolContext) -> dict:
    """
    Vertex AI RAG corporaから、対象となる制度の情報を取得して返す関数

    Args:
        query (str): 類似度検索対象文
        tool_context (ToolContext): The tool context

    Returns:
        dict: {"policies": RAG検索結果}
    """

    # RAG検索
    response = rag.retrieval_query(
        rag_resources=[rag.RagResource(rag_corpus=GOOGLE_RAG_CORPUS_NAME)],
        text=query,
        rag_retrieval_config=rag.RagRetrievalConfig(
            top_k=3,
        ),
    )

    result = [
        {
            "content": ctx.text,  # 取り出したチャンク本文
            # "uri": ctx.source_uri,  # 元ファイルの GCS URI など
            "score": ctx.score,  # コサイン距離 (小さいほど類似)
        }
        for ctx in response.contexts.contexts
    ]

    return {"policies": result}
