"""장르 기반 추천 Agent — Fan-Out 병렬 경로 #2."""
from google.adk import Agent

from movie_agent.config import FLASH_MODEL, PROMPTS_DIR
from movie_agent.tools.movie_filter import search_by_genre

_INSTRUCTION = (PROMPTS_DIR / "genre.md").read_text(encoding="utf-8")

genre_agent = Agent(
    name="genre_agent",
    model=FLASH_MODEL,
    description="특정 장르(로맨스, 코미디, SF 등) 기반 영화 추천",
    instruction=_INSTRUCTION,
    tools=[search_by_genre],
    output_key="output_genre",
)
