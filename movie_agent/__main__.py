"""대화형 진입점 — `python -m movie_agent`.

ADK 2.0a1 의 `adk run` CLI 는 event.content.parts.text 만 출력하는데
Workflow 응답이 event.output 에 실려서 화면에 안 보이는 이슈가 있다.
여기서는 Runner 로 직접 호출하고 두 자리 모두 확인해 출력한다.
"""
from __future__ import annotations

import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

load_dotenv()

from movie_agent.agent import root_agent

APP_NAME = "movie_agent"
USER_ID = "local_user"


def _event_text(event) -> str:
    if event.content and event.content.parts:
        text = "".join(p.text or "" for p in event.content.parts)
        if text:
            return text
    out = getattr(event, "output", None)
    if isinstance(out, str):
        return out
    return ""


def _is_final_output(event, root_name: str) -> bool:
    """"워크플로우의 최종 응답만 필터링합니다.
    
    여러 에이전트(mood, genre, curator 등)가 거치는 과정(중간 결과)을 모두 출력하면
    사용자 화면이 지저분해지므로, 최종적으로 root_agent가 내보내는 결과만 확인합니다.
    """
    # event.author가 root_name 이더라도 내부 라우터 노드의 결과(PARALLEL 등)가 섞여 나옵니다.
    # 워크플로우의 찐 최종 결과는 node_info.path가 정확히 root_name(하위 슬래시 없음)일 때입니다.
    if getattr(event, "node_info", None) and getattr(event.node_info, "path", None) == root_name:
        return event.output is not None
    return False


async def main() -> None:
    session_service = InMemorySessionService()
    runner = Runner(agent=root_agent, session_service=session_service, app_name=APP_NAME)
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID)

    print(f"Running {root_agent.name} — 'exit' 입력 시 종료")
    while True:
        try:
            query = input("\n[user]: ").strip()
            # Windows 터미널 한글 입력 시 발생하는 surrogate 오류 방지
            query = query.encode('utf-8', 'surrogateescape').decode('utf-8', 'ignore')
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not query:
            continue
        if query == "exit":
            break

        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=Content(role="user", parts=[Part(text=query)]),
        ):
            # 워크플로우의 '최종 응답' 이벤트만 콕 집어서 출력 (중간 과정 숨김)
            if _is_final_output(event, root_agent.name):
                text = _event_text(event)
                if text:
                    print(f"\n[🍿 추천 결과]:\n{text}")
                    break # 한 번 출력했으면 더 이상 불필요한 이벤트는 무시하고 빠져나갑니다.


if __name__ == "__main__":
    asyncio.run(main())
