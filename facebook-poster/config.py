import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
FONT_DIR = BASE_DIR / "fonts"
DATABASE_FILE = BASE_DIR / "drafts.db"

OUTPUT_DIR.mkdir(exist_ok=True)
FONT_DIR.mkdir(exist_ok=True)

FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = (
    os.getenv("FACEBOOK_ACCESS_TOKEN")
    or os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
    or os.getenv("FACEBOOK_PAGE_TOKEN")
)

NTFY_SERVER = os.getenv("NTFY_SERVER", "https://ntfy.sh").rstrip("/")
NTFY_TOPIC = os.getenv("NTFY_TOPIC")
NTFY_TOKEN = os.getenv("NTFY_TOKEN")

PUBLIC_APP_URL = os.getenv(
    "PUBLIC_APP_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

REVIEW_SECRET = os.getenv("REVIEW_SECRET")

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

POLLINATIONS_BASE_URL = "https://image.pollinations.ai/prompt"
REQUEST_TIMEOUT = 120

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1080
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
IMAGE_QUALITY = 95

GENERATED_IMAGE_NAME = "generated.png"

TITLE_FONT = str(FONT_DIR / "Poppins-Bold.ttf")
SUBTITLE_FONT = str(FONT_DIR / "Poppins-Regular.ttf")

TITLE_FONT_SIZE = 72
SUBTITLE_FONT_SIZE = 42
TITLE_WRAP = 22
SUBTITLE_WRAP = 34
TITLE_Y = 500
SUBTITLE_Y = 760

TITLE_COLOR = "white"
SUBTITLE_COLOR = "white"
OVERLAY_RGBA = (0, 0, 0, 110)# ============================================================
# COST / CACHE CONTROLS
# ============================================================

# Local cache avoids repeated company/research reads and network calls.
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "21600"))  # 6 hours

# Safe daily call ceilings. Override only when genuinely needed.
MAX_NEWS_FETCH_CALLS_PER_DAY = int(os.getenv("MAX_NEWS_FETCH_CALLS_PER_DAY", "10"))
MAX_LLM_GENERATE_CALLS_PER_DAY = int(os.getenv("MAX_LLM_GENERATE_CALLS_PER_DAY", "5"))
MAX_LLM_REVIEW_CALLS_PER_DAY = int(os.getenv("MAX_LLM_REVIEW_CALLS_PER_DAY", "5"))
MAX_IMAGE_GENERATE_CALLS_PER_DAY = int(os.getenv("MAX_IMAGE_GENERATE_CALLS_PER_DAY", "3"))
MAX_FACEBOOK_PUBLISH_CALLS_PER_DAY = int(os.getenv("MAX_FACEBOOK_PUBLISH_CALLS_PER_DAY", "2"))

# Batch analytics: collect locally and summarize instead of invoking AI per event.
ANALYTICS_BATCH_MODE = os.getenv("ANALYTICS_BATCH_MODE", "true").lower() == "true"

# Set false while developing/testing to avoid image API calls.
ENABLE_IMAGE_GENERATION = os.getenv("ENABLE_IMAGE_GENERATION", "true").lower() == "true"
