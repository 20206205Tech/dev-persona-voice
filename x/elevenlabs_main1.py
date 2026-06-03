# """
# Tạo file âm thanh chào (greeting) cho từng persona trong SAMPLE_PERSONA_DATA.

# - edge_tts: dùng Edge TTS (giống app)
# - elevenlabs: dùng API ElevenLabs (cần ELEVENLABS_API_KEY trong .env)

# Chạy (từ thư mục gốc project, cần file .env):
#     uv run python e.py
# """

# import asyncio
# import json
# import os
# import shutil
# import sys
# import time
# import urllib.request
# from pathlib import Path

# _PROJECT_ROOT = Path(__file__).resolve().parent
# _ENV_FILE = _PROJECT_ROOT / ".env"

# if _ENV_FILE.exists():
#     from environs import Env

#     Env().read_env(_ENV_FILE)
# else:
#     print(f"Không tìm thấy {_ENV_FILE}. Tạo .env từ mẫu project rồi chạy lại.")
#     sys.exit(1)

# import data
# from app.audio.core.edge_tts_utils import generate_audio_file

# OUTPUT_DIR = _PROJECT_ROOT / "data" / "greeting_audio"
# ELEVENLABS_MODEL = "eleven_turbo_v2_5"
# ELEVENLABS_DELAY_SEC = 3


# def _output_path(voice_id: str) -> Path:
#     safe_name = voice_id.replace("/", "_")
#     return OUTPUT_DIR / f"{safe_name}.mp3"


# async def _generate_edge_tts(text: str, voice_id: str, output_path: Path) -> None:
#     temp_path = await generate_audio_file(text, voice_id)
#     shutil.copy2(temp_path, output_path)


# def _generate_elevenlabs(
#     text: str, voice_id: str, output_path: Path, api_key: str
# ) -> None:
#     url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
#     body = json.dumps(
#         {
#             "text": text,
#             "model_id": ELEVENLABS_MODEL,
#             "language_code": "vi",
#         }
#     ).encode("utf-8")
#     request = urllib.request.Request(
#         url,
#         data=body,
#         headers={
#             "xi-api-key": api_key,
#             "Content-Type": "application/json",
#             "Accept": "audio/mpeg",
#         },
#         method="POST",
#     )
#     with urllib.request.urlopen(request) as response:
#         audio_bytes = response.read()
#     output_path.write_bytes(audio_bytes)


# async def generate_greeting_audio_for_persona(
#     persona: data.DataPersona, elevenlabs_api_key: str | None
# ) -> Path:
#     output_path = _output_path(persona.voice_id)
#     OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

#     print(f"[{persona.name}] engine={persona.tts_engine} voice={persona.voice_id}")
#     print(f"  text: {persona.greeting_text}")

#     if persona.tts_engine == "edge_tts":
#         await _generate_edge_tts(
#             persona.greeting_text, persona.voice_id, output_path
#         )
#     elif persona.tts_engine == "elevenlabs":
#         if not elevenlabs_api_key:
#             raise ValueError(
#                 "Thiếu ELEVENLABS_API_KEY trong .env (cần cho persona ElevenLabs)"
#             )
#         _generate_elevenlabs(
#             persona.greeting_text,
#             persona.voice_id,
#             output_path,
#             elevenlabs_api_key,
#         )
#         time.sleep(ELEVENLABS_DELAY_SEC)
#     else:
#         raise ValueError(f"Engine không hỗ trợ: {persona.tts_engine}")

#     print(f"  -> Đã lưu: {output_path}\n")
#     return output_path


# async def main() -> None:
#     elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY", "").strip() or None
#     personas = data.SAMPLE_PERSONA_DATA

#     print(f"Tạo {len(personas)} file greeting audio -> {OUTPUT_DIR}\n")

#     for persona in personas:
#         try:
#             await generate_greeting_audio_for_persona(persona, elevenlabs_api_key)
#         except Exception as e:
#             print(f"  LỖI [{persona.name}]: {e}\n")

#     print("Hoàn thành!")


# if __name__ == "__main__":
#     asyncio.run(main())
