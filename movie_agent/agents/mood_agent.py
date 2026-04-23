"""분위기 기반 추천 Agent — Fan-Out 병렬 경로 #1."""
from google.adk import Agent

from movie_agent.config import FLASH_MODEL, PROMPTS_DIR
from movie_agent.tools.movie_filter import search_by_mood

_INSTRUCTION = (PROMPTS_DIR / "mood.md").read_text(encoding="utf-8")

mood_agent = Agent(
    name="mood_agent",
    model=FLASH_MODEL,
    description="분위기·감성 키워드 기반 영화 추천",
    instruction=_INSTRUCTION,
    tools=[search_by_mood],
    output_key="output_mood",
)
