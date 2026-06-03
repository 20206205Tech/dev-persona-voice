from pathlib import Path
from loguru import logger
from r2_uploader import R2Uploader
import env

def main():
    logger.info("🚀 BẮT ĐẦU ĐỒNG BỘ TOÀN BỘ DỮ LIỆU TRONG /data")
    
    data_dir = Path("data")
    if not data_dir.exists() or not data_dir.is_dir():
        logger.error("Không tìm thấy thư mục 'data'. Vui lòng kiểm tra lại đường dẫn.")
        return

    # Quét đệ quy tất cả các file trong thư mục data
    all_files = [f for f in data_dir.rglob("*") if f.is_file()]
    
    if not all_files:
        logger.warning("Thư mục 'data' trống hoặc không có file nào để upload.")
        return

    logger.info(f"Tìm thấy {len(all_files)} file trong 'data' để xử lý.")

    # Cache các uploader để tránh khởi tạo lại kết nối nhiều lần
    uploaders = {}
    
    def get_uploader(tag: str) -> R2Uploader:
        if tag not in uploaders:
            uploaders[tag] = R2Uploader(metadata_tag=tag)
        return uploaders[tag]

    success_count = 0
    fail_count = 0

    for file_path in all_files:
        # Tính toán relative path so với thư mục 'data'
        try:
            relative_path = file_path.relative_to(data_dir)
        except ValueError as e:
            logger.error(f"Lỗi khi tính toán relative path cho {file_path}: {e}")
            fail_count += 1
            continue

        file_key = relative_path.as_posix()
        
        # Xác định metadata tag dựa trên thư mục con đầu tiên của relative_path
        first_part = relative_path.parts[0] if relative_path.parts else ""
        
        if first_part == "avatars":
            tag = "avatar-sync-script"
        elif first_part == "edge_tts":
            tag = "edge-tts-sync-script"
        elif first_part == "models":
            tag = "model-sync-script"
        else:
            tag = f"{first_part}-sync-script" if first_part else "data-sync-script"

        uploader = get_uploader(tag)
        
        if uploader.upload_file(file_path, file_key=file_key):
            success_count += 1
        else:
            fail_count += 1

    logger.info("-" * 40)
    logger.info(
        f"🎉 Hoàn tất đồng bộ toàn bộ thư mục 'data'! Thành công (gồm cả bỏ qua): {success_count} | Thất bại: {fail_count}"
    )
    logger.info("=" * 40)

if __name__ == "__main__":
    main()