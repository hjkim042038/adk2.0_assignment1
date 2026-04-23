"""Pydantic 스키마 — ADK 2.0 output_schema 용 (claude.md §1)."""
from typing import List, Literal

from pydantic import BaseModel, Field


class Intent(BaseModel):
    """사용자 의도 분석 결과.

    intent_classifier 가 이 형식으로 응답하면 output_key="output_intent" 설정에 따라
    state["output_intent"] 에 dict 로 저장되어 하위 에이전트들이 자동 주입 받음 (claude.md §12).

    각 필드는 담당 하위 에이전트가 state 에서 자기 필드만 읽어 활용:
        - intent_type   → router
        - target_moods  → mood_agent
        - target_genres → genre_agent
        - search_keywords → trending_agent
        - reasoning     → curator_agent
    """

    intent_type: Literal["SIMPLE", "PARALLEL"] = Field(
        description='"SIMPLE"=trending 만 실행 / "PARALLEL"=mood+genre 병렬 후 curator 병합'
    )

    target_moods: List[str] = Field(
        default_factory=list,
        description='분위기/감성 키워드 리스트. 예: ["감성적", "몽환적"]. 가데이터 moods 필드와 매칭.',
    )

    target_genres: List[str] = Field(
        default_factory=list,
        description='장르 키워드 리스트. 예: ["로맨스", "SF"]. 가데이터 genres 필드와 매칭.',
    )

    search_keywords: List[str] = Field(
        default_factory=list,
        description='감독/배우/시대 등 자유 검색 키워드. 예: ["크리스토퍼 놀란", "2010년대"]',
    )

    reasoning: str = Field(
        description="intent_type 분류 및 키워드 추출 근거 (1-2문장). curator 가 최종 이유 작성 시 참고."
    )
