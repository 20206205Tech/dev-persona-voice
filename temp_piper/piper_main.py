import wave
from pathlib import Path

import piper_data
import piper_env
import requests
from loguru import logger
from piper.voice import PiperVoice


def download_file(url: str, dest_path: Path):
    """Hàm hỗ trợ tải file an toàn với stream=True"""
    if dest_path.exists():
        return

    logger.info(f"⏳ Đang tải: {url}")
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(dest_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        logger.success(f"✅ Đã tải xong: {dest_path.name}")
    except Exception as e:
        logger.error(f"❌ Lỗi tải file {url}: {e}")
        raise e


def main():
    logger.info(f"Tổng số Persona: {len(piper_data.SAMPLE_PERSONA_DATA)}")
    logger.info(f"Tổng số Voice: {len(piper_data.SAMPLE_VOICE_DATA)}")

    # Tạo các thư mục cần thiết trong data/
    data_dir = Path(piper_env.PATH_FOLDER_DATA)
    models_dir = data_dir / "models"
    output_dir = data_dir / "greeting_audio"

    models_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Tạo dictionary để map UUID dễ dàng tra cứu
    voices_by_uuid = {v.voice_uuid: v for v in piper_data.SAMPLE_VOICE_DATA}
    engines_by_id = {e.id: e for e in piper_data.SAMPLE_ENGINE_DATA}

    logger.info(f"Bắt đầu xử lý âm thanh. Thư mục lưu: {output_dir}\n" + "-" * 40)

    # 2. Xử lý từng persona
    for persona in piper_data.SAMPLE_PERSONA_DATA:
        # Lấy thông tin Voice và Engine tương ứng
        voice = voices_by_uuid.get(persona.voice_uuid)
        if not voice:
            logger.warning(f"⚠️ Không tìm thấy voice cho persona {persona.name}")
            continue

        engine = engines_by_id.get(voice.engine_id)
        if not engine:
            continue

        # 3. Bỏ qua nếu không phải là engine piper_tts
        if engine.code != "piper_tts":
            logger.info(f"⏭️ Bỏ qua [{persona.name}] (Engine: {engine.code})")
            continue

        voice_code = voice.voice_code  # Tên model (vd: banmai, yannew)
        logger.info(f"🎙️ Đang xử lý Persona: [{persona.name}] - Model: {voice_code}")

        # Đường dẫn file model cục bộ
        model_path = models_dir / f"{voice_code}.onnx"
        config_path = models_dir / f"{voice_code}.onnx.json"

        # Đường dẫn file âm thanh đầu ra (.wav vì Piper dùng định dạng wave)
        output_file = output_dir / f"{voice_code}.wav"

        # Kiểm tra audio đã tồn tại chưa
        if output_file.exists():
            logger.info(f"  ✔️ Audio đã có sẵn: {output_file.name}, bỏ qua.\n")
            continue

        # 4. Tự động tải Model và Config nếu chưa có trong máy
        model_url = f"{piper_env.R2_PUBLIC_DOMAIN}/models/{voice_code}.onnx"
        config_url = f"{piper_env.R2_PUBLIC_DOMAIN}/models/{voice_code}.onnx.json"

        try:
            download_file(model_url, model_path)
            download_file(config_url, config_path)
        except Exception:
            logger.error(f"  ⏭️ Bỏ qua {persona.name} do lỗi tải model.\n")
            continue

        # 5. Khởi tạo PiperVoice và tạo âm thanh
        logger.info(f"  ⚙️ Đang synthesize audio cho '{persona.name}'...")
        try:
            piper_voice = PiperVoice.load(str(model_path), config_path=str(config_path))

            with wave.open(str(output_file), "wb") as wav_file:
                piper_voice.synthesize_wav(persona.greeting_text, wav_file)

            logger.success(f"  ✅ Đã lưu xong: {output_file}\n")

        except Exception as e:
            logger.error(f"  ❌ Lỗi khi generate audio cho {persona.name}: {e}\n")

    logger.info("-" * 40)
    logger.info("🎉 Hoàn thành tất cả các thao tác với Piper TTS!")


if __name__ == "__main__":
    main()
