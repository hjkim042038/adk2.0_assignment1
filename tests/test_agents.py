"""스모크 테스트.

먼저 tool 함수부터 확인 (LLM 안 거침).
Workflow 전체 테스트는 Runner API (claude.md §11) 확인 후 작성.
"""

# from movie_agent.tools.movie_filter import search_by_mood, search_by_genre, search_trending


# def test_mood_filter():
#     result = search_by_mood("감성적")
#     assert len(result) > 0
#     assert all("감성적" in m["moods"] for m in result)


# def test_genre_filter():
#     result = search_by_genre("로맨스")
#     assert len(result) > 0
#     assert all("로맨스" in m["genres"] for m in result)


# def test_trending_filter():
#     result = search_trending(top_k=3)
#     assert len(result) == 3
#     # 평점 내림차순
#     ratings = [m["rating"] for m in result]
#     assert ratings == sorted(ratings, reverse=True)
