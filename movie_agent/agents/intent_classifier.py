"""의도 분류 Agent — SIMPLE vs PARALLEL (claude.md §1)."""
from google.adk import Agent

from movie_agent.config import FLASH_MODEL, PROMPTS_DIR
from movie_agent.schemas import Intent

_INSTRUCTION = (PROMPTS_DIR / "intent.md").read_text(encoding="utf-8")

intent_classifier = Agent(
    name="intent_classifier",
    model=FLASH_MODEL,
    description="사용자 요청을 분석해 경로 + 분위기/장르/검색 키워드 + 근거를 추출",
    instruction=_INSTRUCTION,
    output_schema=Intent,
    output_key="output_intent",
)
