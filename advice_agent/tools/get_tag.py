"""
ユーザーの質問文に関連するタグを抽出するツール
"""

from google import genai
from google.genai.types import HttpOptions, GenerateContentConfig
from google.adk.tools.tool_context import ToolContext

import os
from dotenv import load_dotenv

# 環境変数 GOOGLE_CLOUD_PROJECT / LOCATION　を設定
client = genai.Client(http_options=HttpOptions(api_version="v1"))

# タグとその内容
categories_and_content = {
    "その他サービス": "職業訓練や専門機関委託など、他のカテゴリに当てはまらない支援サービス全般",
    "事業相談": "中小企業者等を対象とした経営や事業運営に関する無料相談窓口",
    "手続きの期限延長": "助成申請や検査等の手続きにおける申請期限や対象期間を延長する措置",
    "支払いの減免・猶予": "住宅使用料や公共料金などの支払いを減額・猶予する支援制度",
    "施設": "宿泊施設等の利用支援や公共施設の活用支援などの施設関連サービス",
    "暮らしの相談": "生活全般の困りごとを相談できる窓口やサポートセンター",
    "生活支援サービス": "育児用品の提供や子育て支援サービスなど日常生活の支援サービス",
    "生活物資の支給": "マスクや食料など生活必需品を無償で配布する支給制度",
    "税制優遇・特例措置": "固定資産税など税負担を軽減する特例措置や優遇措置",
    "給付・助成": "個人・事業者向けの金銭的支給や助成金制度",
    "行政からのお知らせ": "政府・自治体が発信する最新情報や制度案内のお知らせ",
    "補助金": "特定の経費を対象に支給される補助金制度",
    "貸付・融資": "利子補給を含む無利子・低利融資などの貸付制度",
}

PROMPT_TEMPLATE = """
以下のユーザー質問に最も関連するカテゴリ語を返してください。
対象カテゴリは、各カテゴリの内容を読み、ユーザー質問に最も関連するカテゴリを選択してください。
カテゴリは以下の通りです。
{categories_and_content}

例：ユーザー質問：農林漁業にたいするコロナウイルス対策資金支援があれば教えてください。
返答："貸付・融資

ユーザー質問：
\"\"\"{query}\"\"\"

注意点：
対応するカテゴリがなかったときは、『無し』と返してください。
"""


def suggest_tag(user_text: str, tool_context: ToolContext) -> dict:
    """
    質問文を読み取り、categories_andcontentから最も適切なキーを返すツール

    Args:
        user_text (str): ユーザーの質問文
        tool_context (ToolContext): The tool context

    Returns:
        dict: {"tags": "ユーザーの質問文に対応するキー"}
    """

    # プロンプト作成
    prompt = PROMPT_TEMPLATE.format(
        categories_and_content=categories_and_content, query=user_text
    )

    # キーワード抽出
    resp = client.models.generate_content(
        model="gemini-2.5-flash-preview-04-17",
        contents=prompt,
        config=GenerateContentConfig(temperature=0.4),
    )

    keyword = resp.text.strip().strip('"').strip("'")

    return {"tags": keyword}
