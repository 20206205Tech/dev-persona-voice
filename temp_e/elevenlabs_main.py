# import elevenlabs_data


# print(elevenlabs_data.SAMPLE_PERSONA_DATA)
# print(elevenlabs_data.SAMPLE_ENGINE_DATA)

# # Nếu là edge_tts thì tạm thời bỏ qua
# # Nếu là elevenlabs thì tạo file audio với voice_id

import time
from pathlib import Path

import elevenlabs_data
import elevenlabs_env
from elevenlabs.client import ElevenLabs


def main():
    print(f"Tổng số Persona: {len(elevenlabs_data.SAMPLE_PERSONA_DATA)}")
    print(f"Tổng số Engine: {len(elevenlabs_data.SAMPLE_ENGINE_DATA)}\n")

    # Lấy API Key từ cấu hình môi trường đã load trong elevenlabs_env
    api_key = elevenlabs_env.ELEVENLABS_API_KEY
    if not api_key:
        print("❌ LỖI: Vui lòng cung cấp ELEVENLABS_API_KEY trong file .env.")
        return

    # Khởi tạo client ElevenLabs
    client = ElevenLabs(api_key=api_key)

    # Khởi tạo thư mục lưu file audio (sử dụng data/audio ở thư mục gốc của project)
    output_dir = Path(elevenlabs_env.PATH_FOLDER_PROJECT).parent / "data" / "audio"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Map engine_id -> DataEngine
    engine_map = {e.id: e for e in elevenlabs_data.SAMPLE_ENGINE_DATA}
    # Map voice_uuid -> DataVoice
    voice_map = {v.voice_uuid: v for v in elevenlabs_data.SAMPLE_VOICE_DATA}

    print(f"Bắt đầu tạo audio. Thư mục lưu: {output_dir}\n" + "-" * 40)

    # Xử lý từng persona trong dữ liệu mẫu
    for persona in elevenlabs_data.SAMPLE_PERSONA_DATA:
        voice = voice_map.get(persona.voice_uuid)
        if not voice:
            print(f"❌ LỖI: Không tìm thấy voice cho persona '{persona.name}'.\n")
            continue

        engine = engine_map.get(voice.engine_id)
        if not engine:
            print(f"❌ LỖI: Không tìm thấy engine cho voice '{voice.voice_code}'.\n")
            continue

        voice_code = voice.voice_code
        tts_engine = engine.code

        print(f"Đang xử lý Persona: [{persona.name}] - Voice ID: {voice_code}")

        # 1. Nếu là edge_tts hoặc piper_tts thì tạm thời bỏ qua
        if tts_engine in ("edge_tts", "piper_tts"):
            print(f" ⏭️ Bỏ qua (Engine: {tts_engine})\n")
            continue

        # 2. Nếu là elevenlabs thì tạo file audio với voice_code
        if tts_engine == "elevenlabs":
            file_name = output_dir / f"{voice_code}.mp3"

            # Kiểm tra xem file đã được tạo chưa để tránh gọi API trùng lặp gây tốn credit
            if file_name.exists():
                print(f" ⚠️ File {file_name.name} đã tồn tại, bỏ qua.\n")
                continue

            print(f" ⏳ Đang gọi API ElevenLabs cho '{persona.name}'...")
            try:
                # Gọi API chuyển văn bản thành giọng nói
                audio_generator = client.text_to_speech.convert(
                    text=persona.greeting_text,
                    voice_id=voice_code,
                    language_code="vi",
                    model_id="eleven_turbo_v2_5",
                )

                # Lưu luồng dữ liệu (chunk) vào file mp3
                with open(file_name, "wb") as f:
                    for chunk in audio_generator:
                        if chunk:
                            f.write(chunk)

                print(f" ✅ Đã lưu xong: {file_name}\n")

                # Tạm dừng 1.5 giây giữa các request để tránh rate limit của ElevenLabs
                time.sleep(1.5)

            except Exception as e:
                print(f" ❌ Lỗi khi xử lý {persona.name} ({voice_code}): {e}\n")

    print("-" * 40 + "\n🎉 Hoàn thành tất cả các thao tác!")


if __name__ == "__main__":
    main()
