import wave
from pathlib import Path

from piper.voice import PiperVoice


def main():
    # Nội dung văn bản cần đọc
    text = "Xin chào, tôi là trợ lý pháp luật. Bạn có cần tôi giúp đỡ gì không?"

    # Định nghĩa các thư mục
    models_dir = Path("./models")
    output_dir = Path("./output")

    # Tạo thư mục output nếu chưa tồn tại
    output_dir.mkdir(parents=True, exist_ok=True)

    # Lấy danh sách tất cả các file .onnx trong thư mục models
    onnx_files = list(models_dir.glob("*.onnx"))

    if not onnx_files:
        print("Không tìm thấy model nào trong thư mục ./models/")
        return

    print(f"Tìm thấy {len(onnx_files)} models. Đang tiến hành tạo audio...\n")

    # Duyệt qua từng model
    for model_path in onnx_files:
        model_name = model_path.stem  # Lấy tên file không có phần mở rộng .onnx
        config_path = model_path.with_suffix(".onnx.json")

        # Kiểm tra xem file config JSON có tồn tại không
        if not config_path.exists():
            print(f"[Lỗi] {model_name}: Không tìm thấy file config {config_path.name}")
            continue

        output_file = output_dir / f"output_{model_name}.wav"

        # KIỂM TRA FILE ĐÃ TỒN TẠI HAY CHƯA
        if output_file.exists():
            print(f"[Đã có sẵn] {model_name}: Bỏ qua để tiết kiệm tài nguyên.")
            continue

        print(f"Đang xử lý giọng: {model_name}...")
        try:
            # Tải model (Chỉ tải khi chắc chắn cần tạo file mới)
            voice = PiperVoice.load(str(model_path), config_path=str(config_path))

            # Synthesize và lưu file
            with wave.open(str(output_file), "wb") as wav_file:
                voice.synthesize_wav(text, wav_file)

            print(f"  -> Thành công: Đã lưu {output_file.name}")

        except Exception as e:
            print(f"  -> LỖI khi xử lý {model_name}: {e}")

    print("\nHoàn tất! Các file âm thanh đã được lưu trong thư mục /output/")


if __name__ == "__main__":
    main()
