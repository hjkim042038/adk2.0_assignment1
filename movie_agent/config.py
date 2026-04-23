"""프로젝트 전역 설정."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# LLM 모델명
# flash-lite 는 tool 결과 받고도 같은 호출 반복하는 reasoning 한계가 있어 flash 로 상향
FLASH_MODEL = "gemini-2.5-flash"  # 기본 — tool reasoning 안정적
PRO_MODEL = "gemini-2.5-pro"      # 판단력 필요한 Coordinator 등에만

# 가데이터 경로
FAKE_MOVIES_PATH = BASE_DIR / "data" / "fake_movies.json"

# 프롬프트 경로
PROMPTS_DIR = BASE_DIR / "movie_agent" / "prompts"

# AI Studio 키 (GCP 불필요)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
