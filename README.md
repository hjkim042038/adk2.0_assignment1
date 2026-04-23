# ADK 2.0 영화 추천 쇼케이스

이 프로젝트는 영화 추천 시스템을 위해 설계된 ADK 2.0 쇼케이스 저장소입니다. 사용자의 질문 의도에 맞춰 영화 카탈로그를 탐색하고 큐레이션해주는 지능형 다중 에이전트 시스템(Multi-Agent System)의 모범 사례를 담고 있습니다.

모든 추천은 사전에 정의된 `data/fake_movies.json` 가데이터를 기반으로 빠르고 정확하게 이루어집니다.

---

## 🌟 도입된 ADK 2.0 핵심 기능

프로젝트 전반에 걸쳐 ADK 2.0이 제안하는 최신 에이전트 아키텍처가 적용되었습니다.

1. **엄격한 구조화 출력 (`output_schema`)**
    - **적용**: [`intent_classifier`](movie_agent/agents/intent_classifier.py)
    - **효과**: Pydantic 모델을 통한 응답 강제로 파싱 실패율 제로 보장

2. **지능형 도구 추론 (Type hint + Docstring)**
    - **적용**: [`movie_filter.py`](movie_agent/tools/movie_filter.py)
    - **효과**: Python Docstring 만으로 LLM이 도구와 파라미터를 정확히 추론 후 알아서 호출

3. **병렬 분기 및 집결 (Fan-Out / Fan-In)**
    - **적용**: `[mood_agent, genre_agent]` (병렬) → `curator_agent` (집결)
    - **효과**: 독립적인 두 에이전트가 동시에 판단을 내리고 큐레이터가 취합하는 ADK 2.0의 고도화된 다중 에이전트 오케스트레이션

4. **상태 자동 주입 (State Auto-Injection)**
    - **적용**: [`curator_agent`](movie_agent/agents/curator_agent.py)
    - **효과**: 프롬프트 조작 없이 선행 에이전트들의 결과를 자동 참조하여 LLM 환각 최소화

5. **라우터 (Conditional Routing)**
    - **적용**: [`router.py`](movie_agent/router.py)
    - **효과**: 사용자의 의도 분석 결과에 따라 동적인 엣지 분기 수행

---

## 아키텍처

```text
사용자 입력
    ↓
[intent_classifier]       Agent (output_schema=Intent)
    ↓ state["intent"] 에 자동 저장
[intent_router]           함수 — ctx.state 읽고 "SIMPLE" | "PARALLEL" 반환
    │
    ├─ "SIMPLE"   → [trending_agent] → 응답 (단일 경로)
    │
    └─ "PARALLEL" → [mood_agent, genre_agent]   ← Fan-Out (병렬 실행)
                         ↓        ↓
                      [curator_agent]           ← Fan-In (합류 + 큐레이션)
                         ↓
                       응답
```

### 시나리오별 라우팅

| 사용자 입력 예 | intent | 경로 |
|---|---|---|
| "요즘 인기 영화 뭐야" | SIMPLE | trending_agent |
| "평점 높은 거 추천" | SIMPLE | trending_agent |
| "우울할 때 볼 로맨스" | PARALLEL | mood+genre 병렬 → curator |
| "힐링되는 영화 알려줘" | PARALLEL | mood+genre 병렬 → curator |

---

## 빠른 시작

### 1. 가상환경 + 의존성
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. AI Studio API 키 발급 (GCP 불필요, 무료)
https://aistudio.google.com/apikey 에서 키 생성

```bash
cp .env.example .env
# .env 파일 열어서 GOOGLE_API_KEY 채우기
```

### 3. 실행
```bash
# ADK 2.0 의 Runner 로 실행
python -m movie_agent
```

---

## 디렉토리 구조

```text
adk2.0-project1/
├── README.md
├── claude.md                       # ADK 2.0 치트시트
├── requirements.txt
├── .env.example
├── .gitignore
│
├── movie_agent/
│   ├── __init__.py
│   ├── agent.py                    # 워크플로우 정의
│   ├── config.py                   # 환경설정
│   ├── router.py                   # 조건부 라우팅
│   ├── schemas.py                  # Pydantic 스키마
│   │
│   ├── agents/                     # LLM 에이전트 모음
│   │   ├── intent_classifier.py    
│   │   ├── mood_agent.py           
│   │   ├── genre_agent.py          
│   │   ├── trending_agent.py       
│   │   └── curator_agent.py        
│   │
│   ├── tools/                      # 필터 도구
│   │   └── movie_filter.py
│   │
│   └── prompts/                    # 프롬프트 저장소
│
├── data/
│   └── fake_movies.json            # 가데이터
│
└── tests/
    └── test_agents.py              # 테스트
```

---

## 중요 메모

- ADK 2.0 API에 맞게 업그레이드 및 작성되었습니다.
- LLM 모델은 경량 모델(Flash)을 기본으로 안정감 있게 동작하도록 설계되었습니다.
- API 호출이 없으므로 추가 과금이 발생하지 않습니다.
