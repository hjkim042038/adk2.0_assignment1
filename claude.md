# ADK 2.0 Core Cheatsheet

이 문서는 ADK 2.0 코딩 시 토큰을 절약하기 위한 초압축 가이드입니다. 

### 1. Agent 선언 방식 (output_schema 포함)
```python
from google.adk import Agent
from pydantic import BaseModel

class MyOutput(BaseModel):
    result: str
    
agent = Agent(
    name="my_agent",
    model="gemini-2.5-flash",
    instruction="...",
    tools=[my_tool],
    output_schema=MyOutput, # [💡 핵심] ADK 2.0부터 Pydantic Schema로 LLM 응답 형식을 강제함
)
```

### 2. Tool 함수 정의 패턴 (Type Hint & Docstring)
```python
# 파라미터 타입과 Docstring을 완벽히 작성해야 LLM이 이를 파싱해 올바른 Tool 매개변수를 추론함
def get_weather(city: str) -> dict:
    """Get weather info.
    Args:
        city: The city name
    """
    return {"temp": 20, "condition": "Sunny"}
```

### 3. Workflow 흐름 (직렬)
```python
from google.adk import Workflow

workflow = Workflow(
    name="simple_flow",
    edges=[
        ("START", step1_agent),
        (step1_agent, step2_func),
        (step2_func, step3_agent)
    ],
)
```

### 4. Fan-Out / Fan-In 병렬 처리 패턴
```python
# List로 묶인 노드들은 병렬로 동시 실행 (Fan-Out)
# 이후 List 노드들을 다음 단일 노드로 연결하여 병합 (Fan-In)
workflow = Workflow(
    name="parallel_flow",
    edges=[
        ("START", start_agent),
        (start_agent, [node_a, node_b]), # 두 방향 동시 분기
        ([node_a, node_b], join_node)    # 두 처리 결과 취합
    ]
)
```

### 5. Node 생성 방식 (함수형 / BaseNode 클래스형)
```python
from google.adk.agents import Context, BaseNode

# [함수형] node로 사용시 return된 dict의 key들이 state에 자동 머지됨. 
# state의 key와 함수의 인수가 이름 단위로 매핑되어 자동 주입됨 (Auto-wiring)
def parse_input(applicant_name: str) -> dict:
    return {"parsed_name": applicant_name.upper()}

# [클래스형] 복잡한 상태 주입이나 동적 로직이 필요한 경우
class CustomNode(BaseNode):
    def _execute(self, context: Context, **kwargs):
        val = context.state.get("some_key")
        return {"updated_key": val + 1}
```

### 6. 라우팅 조건 함수 시그니처 (Conditional Routing)
```python
# Router 함수는 Context를 받아 '다음 실행할 노드 변수' 혹은 '분기용 문자열 식별자' 리턴
def evaluate_score(ctx: Context) -> str:
    score = ctx.state.get("score", 0)
    return "PASS" if score > 80 else "FAIL"

edges = [
    (node_a, evaluate_score),
    (evaluate_score, {"PASS": pass_node, "FAIL": fail_node}) # dict 기반 조건 분기
]
```

### 7. Context로 상태 (State) 공유하는 패턴
```python
# Node(또는 Agent)의 실행 중에 Context를 통해 전역 State 공유 
def mutate_state(ctx: Context):
    # 방법 1: 직접 할당
    ctx.state["shared_data"] = 100 
    # 방법 2: Dictionary 반환 -> Workflow 엔진이 받아서 강제로 ctx.state.update 수행함
    return {"other_data": 200}
```

### 8. HITL 중단/재개 패턴 (RequestInput 등)
```python
from google.adk.callbacks import RequestInput

# 에이전트 실행 후 사용자 입력 대기로 워크플로우 일시 중지
hitl_agent = Agent(
    name="hitl_agent",
    after_model_call=[RequestInput("추가 정보가 필요합니다: ")]
)
# [재개 방식] 외부 API / Runner에서 session_id로 state_updates 와 함께 resume 호출
# runner.resume(session_id=..., user_id=..., next_node=hitl_agent, state_updates={"input": "..."})
```

### 9. Task 상태 Enum 값 및 위임 (Delegation)
```python
from google.adk.tasks import TaskStatus

# TaskStatus 값: PENDING, IN_PROGRESS, COMPLETED, FAILED, CANCELLED
# Task를 반환하면 워크플로우를 블락하지 않고 외부에 처리를 위임할 수 있음
```

### 10. MCP/A2A 통신 선언과 1.0 → 2.0 주의사항
- **A2A 분산 처리**: `app = agent.to_a2a()` (서버생성) / `RemoteA2aAgent(agent_uri="...")` (클라이언트 연결)
- **MCP 연결**: `MCPTool(name="...", server_url="...")`
- ⚠️ **[CRITICAL] 1.0 → 2.0 마이그레이션 및 데이터 저장소 혼용 금지**: (1) 단일 에이전트도 Workflow 래핑 필수. (2) **Session, Memory, Evaluation Data** 등을 영구 저장하는 시스템은 ADK 1.0 프로젝트와 2.0 프로젝트 간 **절대 혼용(공유) 금지** (스키마 충돌 등 치명적인 데이터 손상 및 파괴 우려).

### 11. Workflow 실행 코드 (Runner API)
```python
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

async def run_workflow(agent, user_message: str):
    session_service = InMemorySessionService()
    runner = Runner(agent=agent, session_service=session_service, app_name="demo")
    session = await session_service.create_session(app_name="demo", user_id="user1")
    
    msg = Content(role="user", parts=[Part(text=user_message)])
    
    # 비동기 제너레이터로 이벤트 스트리밍 수신 (Agent.run() 사용 금지)
    async for event in runner.run_async(user_id="user1", session_id=session.id, new_message=msg):
        if event.content and event.content.parts:
            print(event.content.parts[0].text)
```

### 12. State 자동 주입 (Auto-Injection) 원리
- Function 노드가 `{"score": 800}` 형태의 Dict를 리턴하면 워크플로우에 의해 `Context.state["score"]`에 자동 저장됩니다.
- **[💡 환각 방지 핵심]**: 이 뒤에 바로 연결된 LLM Agent 노드는, 프롬프트에 `{score}`라고 포맷팅을 해주지 않아도 **현재의 전체 `state`가 암묵적인 Context로 LLM에게 자동 주입**됩니다. 따라서 "이전 결과를 분석해줘"라는 Instruction 만으로 알아서 값을 인지하고 동작합니다.

### 13. Coordinator Agent (AutoFlow 라우팅) 패턴
```python
# 선을 긋는 Workflow(Graph) 방식이 아니라,
# LLM이 하위 Agent들의 `description`을 읽고 스스로 판단해 동적으로 임무를 위임하는 아키텍처
researcher = Agent(name="R", description="리서치와 팩트 체크가 필요할 때 호출", ...)
writer = Agent(name="W", description="대본이나 글쓰기가 필요할 때 호출", ...)

coordinator = Agent(
    name="director",
    model="gemini-2.5-pro", # 판단력이 좋은 Pro 모델 사용 필수
    instruction="1. 조사 후 2. 글을 작성하도록 지시해",
    sub_agents=[researcher, writer] # 엣지 연결 없이 여기에만 선언하면 알아서 AutoFlow 동작
)
```
