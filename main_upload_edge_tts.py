import mimetypes
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from loguru import logger

# Nạp cấu hình từ file env.py cùng thư mục
import env

# Cấu hình R2 - Lấy trực tiếp từ module env
R2_ENDPOINT_URL = env.R2_ENDPOINT_URL
R2_ACCESS_KEY_ID = env.R2_ACCESS_KEY_ID
R2_SECRET_ACCESS_KEY = env.R2_SECRET_ACCESS_KEY

# Tự động chọn Bucket dựa trên ENVIRONMENT
BUCKET_NAME = "dev-persona" if env.ENVIRONMENT == "development" else "prod-persona"


class R2EdgeTTSUploader:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=R2_ENDPOINT_URL,
            aws_access_key_id=R2_ACCESS_KEY_ID,
            aws_secret_access_key=R2_SECRET_ACCESS_KEY,
            region_name="auto",
        )
        logger.success(f"Đã khởi tạo kết nối Cloudflare R2 - Bucket: {BUCKET_NAME}")

    def get_content_type(self, filepath: Path) -> str:
        # Xác định Content-Type ưu tiên cho các định dạng ảnh phổ biến (trong edge_tts là .png)
        ext = filepath.suffix.lower()
        if ext in [".jpg", ".jpeg"]:
            return "image/jpeg"
        elif ext == ".png":
            return "image/png"
        elif ext == ".webp":
            return "image/webp"

        mime_type, _ = mimetypes.guess_type(filepath)
        return mime_type or "application/octet-stream"

    def upload_file(self, file_path: Path) -> bool:
        """Upload một file vật lý từ thư mục edge_tts lên R2"""
        # Giữ nguyên cấu trúc thư mục, ví dụ: file trong edge_tts/vi-VN-HoaiMyNeural-v1.png
        # sẽ có key là edge_tts/vi-VN-HoaiMyNeural-v1.png
        file_key = file_path.as_posix()
        content_type = self.get_content_type(file_path)

        try:
            logger.info(f"📤 Đang upload: {file_key}")

            # Mở file dưới dạng binary và upload
            with open(file_path, "rb") as file_obj:
                self.client.upload_fileobj(
                    file_obj,
                    BUCKET_NAME,
                    file_key,
                    ExtraArgs={
                        "ContentType": content_type,
                        "Metadata": {"uploaded-by": "edge-tts-sync-script"},
                    },
                )
            logger.success(f"✅ Upload thành công: {file_key}")
            return True

        except ClientError as e:
            logger.error(f"❌ Lỗi khi upload {file_key}: {e}")
            return False


def main():
    edge_tts_dir = Path("./edge_tts")

    if not edge_tts_dir.exists() or not edge_tts_dir.is_dir():
        logger.error(
            "Không tìm thấy thư mục 'edge_tts'. Vui lòng kiểm tra lại đường dẫn."
        )
        return

    # Khởi tạo Uploader
    uploader = R2EdgeTTSUploader()

    # Quét toàn bộ file trong thư mục edge_tts
    edge_tts_files = [f for f in edge_tts_dir.iterdir() if f.is_file()]

    if not edge_tts_files:
        logger.warning("Thư mục 'edge_tts' trống. Không có gì để upload.")
        return

    logger.info(f"Tìm thấy {len(edge_tts_files)} file cần upload.")

    success_count = 0
    fail_count = 0

    # Tiến hành upload từng file
    for file_path in edge_tts_files:
        if uploader.upload_file(file_path):
            success_count += 1
        else:
            fail_count += 1

    logger.info("=" * 40)
    logger.info(
        f"🎉 Hoàn tất upload! Thành công: {success_count} | Thất bại: {fail_count}"
    )


if __name__ == "__main__":
    main()
