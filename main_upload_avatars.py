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


class R2AvatarUploader:
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
        # Xác định Content-Type ưu tiên cho các định dạng ảnh phổ biến
        ext = filepath.suffix.lower()
        if ext in [".jpg", ".jpeg"]:
            return "image/jpeg"
        elif ext == ".png":
            return "image/png"
        elif ext == ".webp":
            return "image/webp"

        mime_type, _ = mimetypes.guess_type(filepath)
        return mime_type or "application/octet-stream"

    def file_exists(self, file_key: str) -> bool:
        """Kiểm tra xem object đã tồn tại trên R2 chưa bằng cách đọc metadata"""
        try:
            self.client.head_object(Bucket=BUCKET_NAME, Key=file_key)
            return True
        except ClientError as e:
            # Mã lỗi 404 Not Found có nghĩa là file chưa tồn tại
            if e.response["Error"]["Code"] == "404":
                return False
            # Nếu gặp lỗi khác (ví dụ: sai quyền truy cập, lỗi mạng), log ra để kiểm tra
            logger.error(f"Lỗi khi kiểm tra tồn tại của {file_key}: {e}")
            return False

    def upload_file(self, file_path: Path) -> bool:
        """Upload một file avatar vật lý lên R2 (bỏ qua nếu đã có)"""
        file_key = file_path.as_posix()

        # 1. KIỂM TRA FILE ĐÃ TỒN TẠI CHƯA
        if self.file_exists(file_key):
            logger.info(f"⏭️ Bỏ qua (Đã tồn tại): {file_key}")
            # Vẫn trả về True vì mục tiêu cuối cùng là file đã có mặt trên R2
            return True

        # 2. TIẾN HÀNH UPLOAD NẾU CHƯA CÓ
        content_type = self.get_content_type(file_path)

        try:
            logger.info(f"📤 Đang upload: {file_key}")

            with open(file_path, "rb") as file_obj:
                self.client.upload_fileobj(
                    file_obj,
                    BUCKET_NAME,
                    file_key,
                    ExtraArgs={
                        "ContentType": content_type,
                        "Metadata": {"uploaded-by": "avatar-sync-script"},
                    },
                )
            logger.success(f"✅ Upload thành công: {file_key}")
            return True

        except ClientError as e:
            logger.error(f"❌ Lỗi khi upload {file_key}: {e}")
            return False


def main():
    avatars_dir = Path("./avatars")

    if not avatars_dir.exists() or not avatars_dir.is_dir():
        logger.error(
            "Không tìm thấy thư mục 'avatars'. Vui lòng kiểm tra lại đường dẫn."
        )
        return

    # Khởi tạo Uploader
    uploader = R2AvatarUploader()

    # Quét toàn bộ file trong thư mục avatars
    avatar_files = [f for f in avatars_dir.iterdir() if f.is_file()]

    if not avatar_files:
        logger.warning("Thư mục 'avatars' trống. Không có gì để upload.")
        return

    logger.info(f"Tìm thấy {len(avatar_files)} file để xử lý.")

    success_count = 0
    fail_count = 0

    # Tiến hành upload từng file
    for file_path in avatar_files:
        if uploader.upload_file(file_path):
            success_count += 1
        else:
            fail_count += 1

    logger.info("=" * 40)
    logger.info(
        f"🎉 Hoàn tất! Thành công (gồm cả bỏ qua): {success_count} | Thất bại: {fail_count}"
    )


if __name__ == "__main__":
    main()
