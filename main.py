"""
GPT-6 Astra Tester - Force Image Generation
"""

import os
import base64
import mimetypes
from pathlib import Path
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-6-astra"

OUTPUT_DIR = Path("generated_images")
OUTPUT_DIR.mkdir(exist_ok=True)


def encode_image(image_path: str) -> str:
    path = Path(image_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    mime_type, _ = mimetypes.guess_type(str(path))
    if not mime_type or not mime_type.startswith("image/"):
        ext = path.suffix.lower()
        mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
                    ".webp": "image/webp", ".gif": "image/gif"}
        mime_type = mime_map.get(ext, "image/jpeg")

    print(f"📷 Loading: {path.name}")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{b64}"


def save_generated_image(base64_data: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUT_DIR / f"astra_{timestamp}.png"
    with open(filename, "wb") as f:
        f.write(base64.b64decode(base64_data))
    return str(filename)


def ask_astra(prompt: str, image_path: str | None = None, effort: str = "medium", force_generate: bool = False):
    print(f"\n🤖 GPT-6 Astra ({effort} effort) is thinking...\n")