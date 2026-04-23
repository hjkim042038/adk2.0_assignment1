"""가데이터 영화 리스트 필터 함수 모음 (claude.md §2).

ADK 2.0 Tool 규칙:
  - 파라미터에 **type hint** 필수
  - **docstring** 에 Args 설명 필수 → LLM 이 이걸 보고 파라미터 추론함
"""
import json
from functools import lru_cache

from movie_agent.config import FAKE_MOVIES_PATH


@lru_cache(maxsize=1)
def _load_movies() -> list[dict]:
    with open(FAKE_MOVIES_PATH, encoding="utf-8") as f:
        return json.load(f)


def search_by_mood(mood: str) -> list[dict]:
    """Search movies matching a mood keyword.

    Args:
        mood: Korean mood keyword such as "감성적", "유쾌한", "우울", "몽환적".
    """
    return [m for m in _load_movies() if mood in m.get("moods", [])]


def search_by_genre(genre: str) -> list[dict]:
    """Search movies matching a genre.

    Args:
        genre: Korean genre name such as "로맨스", "코미디", "SF", "액션".
    """
    return [m for m in _load_movies() if genre in m.get("genres", [])]


def search_trending(top_k: int = 5) -> list[dict]:
    """Return top-rated movies (mocking trending data).

    Args:
        top_k: Number of movies to return. Defaults to 5.
    """
    return sorted(_load_movies(), key=lambda m: m.get("rating", 0), reverse=True)[:top_k]
