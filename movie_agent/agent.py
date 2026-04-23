"""Root Workflow — ADK 2.0 그래프 선언 (claude.md §3, §4, §6).

그래프:
    START
      → intent_classifier (Agent, output_schema=Intent)
      → intent_router (함수)
        ├─ "SIMPLE"   → trending_agent (단일 경로 종료)
        └─ "PARALLEL" → [mood_agent, genre_agent]  ← Fan-Out
                           → curator_agent         ← Fan-In
"""
from google.adk import Workflow

from movie_agent.agents.intent_classifier import intent_classifier
from movie_agent.agents.mood_agent import mood_agent
from movie_agent.agents.genre_agent import genre_agent
from movie_agent.agents.trending_agent import trending_agent
from movie_agent.agents.curator_agent import curator_agent
from movie_agent.router import intent_router

root_agent = Workflow(
    name="movie_recommendation_workflow",
    edges=[
        ("START", intent_classifier),
        (intent_classifier, intent_router),
        (intent_router, {
            "SIMPLE": trending_agent,
            "PARALLEL": [mood_agent, genre_agent],
        }),
        ([mood_agent, genre_agent], curator_agent),
    ],
)
