import uuid

import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from advice_agent.agent import root_agent as AdviceAgent
# import json

load_dotenv()


async def main():
    # セッションサービスの初期化
    session_service_stateful = InMemorySessionService()

    # 新しいセッションの作成
    APP_NAME = "advice_agent"
    user_ID = "user123"
    SESSION_ID = str(uuid.uuid4())
    # stateful_session = session_service_stateful.create_session_sync(
    stateful_session = await session_service_stateful.create_session(
        app_name=APP_NAME, user_id=user_ID, session_id=SESSION_ID
    )
    print(f"Created new session: {stateful_session}")
    print(f"\tSession ID: {SESSION_ID}")

    # ランナーの初期化
    runner = Runner(
        agent=AdviceAgent,
        session_service=session_service_stateful,
        app_name=APP_NAME,
    )

    while True:
        user_input = input("message: ")
        if user_input.lower() == "exit":
            print("Exiting the application.")
            break

        # user_message_str = json.dumps(user_input)
        user_content = types.Content(role="user", parts=[types.Part(text=user_input)])

        # エージェントの実行
        events = runner.run_async(
            user_id=user_ID,
            session_id=SESSION_ID,
            new_message=user_content,
        )

        async for event in events:
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_answer = event.content.parts[0].text
        print(f"Response: {final_answer}")


if __name__ == "__main__":
    asyncio.run(main())
