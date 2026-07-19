"""Project paths and environment configuration."""
import os
import shutil
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

COMMAND_PREFIX = "$"


def load_token() -> str:
    """Load .env and return the bot token."""
    load_dotenv(PROJECT_ROOT / ".env")
    token = os.getenv("TOKEN")
    if not token:
        raise SystemExit("TOKEN is missing - add it to the .env file.")
    return token


def find_ffmpeg() -> str:
    """Prefer the ffmpeg.exe bundled in the venv, fall back to PATH."""
    bundled = Path(sys.executable).parent / "ffmpeg.exe"
    if bundled.exists():
        return str(bundled)
    return shutil.which("ffmpeg") or "ffmpeg"
