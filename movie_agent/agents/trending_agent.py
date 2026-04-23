"""인기 영화 추천 Agent — SIMPLE 경로 전담."""
from google.adk import Agent

from movie_agent.config import FLASH_MODEL, PROMPTS_DIR
from movie_agent.tools.movie_filter import search_trending

_INSTRUCTION = (PROMPTS_DIR / "trending.md").read_text(encoding="utf-8")

trending_agent = Agent(
    name="trending_agent",
    model=FLASH_MODEL,
    description="요즘 인기 영화, 평점 높은 영화 추천",
    instruction=_INSTRUCTION,
    tools=[search_trending],
)
