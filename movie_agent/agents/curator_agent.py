"""Fan-In 큐레이션 Agent — state auto-injection 쇼케이스 (claude.md §12).

mood_agent 와 genre_agent 의 결과가 state 에 자동 주입되므로,
프롬프트에 명시적으로 {mood_result}, {genre_result} 를 포맷팅하지 않아도
LLM 이 state 전체를 암묵적 컨텍스트로 인지한다.
"""
from google.adk import Agent

from movie_agent.config import FLASH_MODEL, PROMPTS_DIR

_INSTRUCTION = (PROMPTS_DIR / "curator.md").read_text(encoding="utf-8")

curator_agent = Agent(
    name="curator_agent",
    model=FLASH_MODEL,
    description="병렬 추천 결과를 받아 최종 3~5편으로 큐레이션",
    instruction=_INSTRUCTION,
)
