import os
from pathlib import Path
import imageio_ffmpeg

# Base directories
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"
ASSETS_DIR = BASE_DIR / "assets"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# FFmpeg Executable path
try:
    FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_EXE = "ffmpeg"

# Video Settings (9:16 Vertical Short format)
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30
NUM_SCENES = 6
SCENE_DURATION_SEC = 10.0  # 6 scenes x 10s = 60 seconds total

# API Keys (optional; fallback engines handle missing keys)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GOOGLE_FLOW_API_KEY = os.environ.get("GOOGLE_FLOW_API_KEY", "")
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN", "")

# Voice Settings (Hindi Neural Male Influencer Voice)
DEFAULT_VOICE = "hi-IN-MadhurNeural"  # Microsoft Neural Hindi Male Voice via edge-tts
FALLBACK_VOICE = "hi-IN-SwaraNeural"

# Character Lock & Aesthetic
CHARACTER_LOCK_PROMPT = (
    "Use the exact same 22-year-old Indian boy in every scene. "
    "Preserve face, hairstyle, eyes, skin tone, body proportions, clothing, voice, age and identity with 100% consistency."
)

# Colors & Subtitles
PRIMARY_COLOR = "&H00FFFF"  # Yellow in ASS format
SECONDARY_COLOR = "&HFFFFFF"  # White in ASS format
OUTLINE_COLOR = "&H000000"  # Black border
FONT_SIZE = 42
FONT_NAME = "Arial"
