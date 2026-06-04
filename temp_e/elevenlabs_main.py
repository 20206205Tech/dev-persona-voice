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

    # Khởi tạo thư mục lưu file audio (sử dụng PATH_FOLDER_DATA từ elevenlabs_env)
    output_dir = Path(elevenlabs_env.PATH_FOLDER_DATA) / "greeting_audio"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Bắt đầu tạo audio. Thư mục lưu: {output_dir}\n" + "-" * 40)

    # Xử lý từng persona trong dữ liệu mẫu
    for persona in elevenlabs_data.SAMPLE_PERSONA_DATA:
        print(f"Đang xử lý Persona: [{persona.name}] - Voice ID: {persona.voice_id}")

        # 1. Nếu là edge_tts thì tạm thời bỏ qua
        if persona.tts_engine == "edge_tts":
            print(f" ⏭️ Bỏ qua (Engine: {persona.tts_engine})\n")
            continue

        # 2. Nếu là elevenlabs thì tạo file audio với voice_id
        if persona.tts_engine == "elevenlabs":
            file_name = output_dir / f"{persona.voice_id}.mp3"

            # Kiểm tra xem file đã được tạo chưa để tránh gọi API trùng lặp gây tốn credit
            if file_name.exists():
                print(f" ⚠️ File {file_name.name} đã tồn tại, bỏ qua.\n")
                continue

            print(f" ⏳ Đang gọi API ElevenLabs cho '{persona.name}'...")
            try:
                # Gọi API chuyển văn bản thành giọng nói
                audio_generator = client.text_to_speech.convert(
                    text=persona.greeting_text,
                    voice_id=persona.voice_id,
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
                print(f" ❌ Lỗi khi xử lý {persona.name} ({persona.voice_id}): {e}\n")

    print("-" * 40 + "\n🎉 Hoàn thành tất cả các thao tác!")


if __name__ == "__main__":
    main()
