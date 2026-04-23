"""Conditional routing 함수 (claude.md §6, llms.txt Lab 3 패턴).

Router 함수는 직전 노드의 출력 dict 를 받아 Event 를 반환한다.
Event(route=<라벨>, output=<라벨>) 형태일 때 다음 dict edge 의 키와 매칭된다.
"""
from google.adk.events import Event


def intent_router(node_input: dict) -> Event:
    """intent_classifier 출력에서 intent_type 을 꺼내 분기 라벨 emit.

    Args:
        node_input: 직전 노드(intent_classifier) 의 output Intent dict.
            예: {"intent_type": "SIMPLE", "target_moods": [...], ...}
    """
    intent_type = (
        node_input.get("intent_type", "SIMPLE")
        if isinstance(node_input, dict)
        else "SIMPLE"
    )
    if intent_type not in ("SIMPLE", "PARALLEL"):
        intent_type = "SIMPLE"
    return Event(route=intent_type, output=intent_type)
