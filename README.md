# GCP_ADK_Agent_1
* google-adkを用いたGCPでのReact型Agentの実装
* adkにおける、シングルエージェントでのReact型思考による複数関数の利用に関する備忘録

## google-adkについて
* googleのAgentフレームワーク
* シングルエージェントからマルチエージェントまで作成可能
* 制限：
  * built-inツールは、一つしか設定できない
    * 複数のbuilt-inツールを使いたい場合は、それぞれカスタム関数として実装が必要(2025/6時点での制限)
      * 例えば、web検索とRAG検索の両方をツールとして設定したい場合は、built-inとしてではなく、カスタム関数側にweb検索のapiとRAGのapiでそれぞれ呼び出して利用する
* マルチエージェントは、Sequential Agent、Parallel Agent、Loop Agentのインスタンスがあり、それらを利用することで、簡単に作成が可能
  * ただし、マルチエージェントでの、各サブエージェントはbuilt-inツールが使えないため、カスタム関数化が必要(2025/6時点での制限)
* Vertex AIと親和性が高く、デプロイはVertex AI Agent Engineに行う
* sessionとrunner
  * sessionは、Azure AI Foundryの**スレッド**と同じで、会話やツールの実行履歴を保存する
  * runnerは、React等での思考フローに沿った適切なツール実行を管理する
* ローカルでの開発・実行時は、Google Cloud CLIをインストールし、`gcloud auth application-default login』で認証を行うことで、可能となる
  
## google-adkでAgent作成時のファイル構成
* 以下の構成でファイルを作成する必要がある。

```bash
advice_agent/ # このファイル名をagent.pyに設定する                                                
├── .env
├── __init__.py
└── agent.py          
```

## .envの設定内容
* プロジェクト名（GOOGLE_CLOUD_PROJECT）
* リージョン（GOOGLE_GENAI_USE_VERTEXAI）
* RAG Engineのリソース名

## 今回のAgentの内容
* エージェントの役割：質問文に対応する、コロナ対策支援事業を紹介する

### 実装内容
1. 質問に対応するキーワードをLLMが抽出するカスタム関数
   * LLMがキーワードと関連内容の一覧から、質問文にマッチしそうなキーワード抽出する。（このキーワードはRAG検索時の精度向上用）
2. RAG検索カスタム関数
   * make_vector_store.ipynbで作成したRAG Engineを呼び出し、質問文に関連する東京都のコロナ支援制度を検索する
3. 上記２つの関数を用いて、質問文にマッチする支援事業を紹介する

### Agent実装時の注意点
* RAG検索などのbuilt-inツールは、一つしか利用できず、他のbuilt-inツールやカスタム関数との併用はできないため、それぞれカスタム関数化が必要
  * もし、web検索なども併用したい場合は、web検索apiでカスタム関数化が必要

### ファイル構成
```bash
GCP_ADK_AGENT_1/
├── .env
├── make_vector_store.ipynb # RAG Engine作成用notebook
├── main.py # ローカルのcli実行時に必要なsessionとrunnerの設定ファイル (python main.pyでcli実行)
├── data_for_rag/
|     └── merge_tags_content.txt # RAG Engine用元データ（東京都のコロナ対策事業一覧）
└── advice_agent/
      ├── .env
      ├── __init__.py
      ├── agent.py # prompt、agent定義ファイル
      └── tools/
            ├── get_tag.py # キーワード取得用カスタム関数。関数内で別途LLMを呼び出して利用
            └── rag_query.py # RAG検索用カスタム関数

