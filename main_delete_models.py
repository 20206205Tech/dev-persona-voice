from pathlib import Path


def main():
    models_dir = Path("./models")
    output_dir = Path("./output")

    # Kiểm tra xem các thư mục có tồn tại không
    if not models_dir.exists() or not output_dir.exists():
        print("Lỗi: Không tìm thấy thư mục 'models' hoặc 'output'.")
        return

    # 1. Lấy danh sách các model được giữ lại từ thư mục output
    kept_models = set()
    for wav_file in output_dir.glob("output_*.wav"):
        # Tên file có dạng "output_banmai", ta dùng .replace để cắt bỏ "output_"
        model_name = wav_file.stem.replace("output_", "")
        kept_models.add(model_name)

    print(
        f"Tìm thấy {len(kept_models)} file âm thanh. Sẽ giữ lại {len(kept_models)} models này.\n"
    )

    # 2. Quét và xóa các file trong thư mục models không nằm trong danh sách giữ lại
    deleted_count = 0
    for model_file in models_dir.iterdir():
        if not model_file.is_file():
            continue

        # Xác định tên gốc của model từ tên file
        base_name = ""
        if model_file.name.endswith(".onnx.json"):
            base_name = model_file.name.replace(".onnx.json", "")
        elif model_file.name.endswith(".onnx"):
            base_name = model_file.name.replace(".onnx", "")

        # Bỏ qua nếu file có định dạng lạ
        if not base_name:
            continue

        # Xóa file nếu model gốc không có trong tập kept_models
        if base_name not in kept_models:
            print(f"Đang xóa: {model_file.name}")
            model_file.unlink()  # Lệnh xóa file trực tiếp
            deleted_count += 1

    print(
        f"\nHoàn tất! Đã dọn dẹp {deleted_count} file không sử dụng khỏi thư mục /models/."
    )


if __name__ == "__main__":
    main()
