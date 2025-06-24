from google.adk.agents import Agent

from .tools.get_tag import suggest_tag
from .tools.rag_query import search_support_policy_info


instruction = """
あなたはユーザーの質問・相談に対応する東京都のコロナ対策支援事業を紹介するエージェントです。
与えられたユーザーの質問を読み取り、以下のツールを使ってその質問に対応するコロナ対策支援事業を紹介してください。

ツール一覧と使用方法：
1. `suggest_tag(date: str) -> Dict[str, bool]`:ユーザーの質問・相談に対応するキーワード（tags）を選ぶ。
2. `search_support_policy_info(date: str) -> Dict[str, bool]`:タグとユーザーの質問の連結文から類似の文章（支援事業の内容）を抽出する

考え方：
1. まず`suggest_tag`で、ユーザーの質問に対応するキーワード(tags)を選ぶ。
2. 次に、RAG検索の精度が上がるように、suggest_tagで抽出したキーワードとユーザーの質問文を以下のように、連結する。
    - "tags:抽出したキーワード, content:ユーザーの質問文"
3. 2で作成した文章を元に、`search_support_policy_info`で関連する政策情報を取得する。 
4. 必要な情報を得られたら、ユーザーの質問にマッチしている政策事業を提示する。

出力の指示：
該当する政策がなかった場合は、丁寧な表現で、無かった旨伝えてください。

注意点：
`search_support_policy_info`の情報は古いですが、質問する時期をコロナ真っただ中の時期(2023年～2024年)とみなして、質問に答えてください。
"""

root_agent = Agent(
    name="advice_agent",  # agent.pyのフォルダ名と同じにする
    model="gemini-2.5-flash-preview-04-17",
    description="ユーザーの質問・相談に対応するコロナ対策支援事業を紹介するエージェント",
    tools=[
        suggest_tag,
        search_support_policy_info,
    ],
    instruction=instruction,
)
