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


class R2Uploader:
    def __init__(self, metadata_tag: str):
        """
        Khởi tạo uploader với tag siêu dữ liệu (metadata) riêng biệt cho từng loại file.
        """
        self.metadata_tag = metadata_tag
        self.client = boto3.client(
            "s3",
            endpoint_url=R2_ENDPOINT_URL,
            aws_access_key_id=R2_ACCESS_KEY_ID,
            aws_secret_access_key=R2_SECRET_ACCESS_KEY,
            region_name="auto",
        )
        logger.success(
            f"Đã khởi tạo kết nối Cloudflare R2 - Bucket: {BUCKET_NAME} | Tag: {self.metadata_tag}"
        )

    def get_content_type(self, filepath: Path) -> str:
        # Hỗ trợ nhận diện các định dạng cho cả Image, TTS và Model
        ext = filepath.suffix.lower()
        if ext in [".jpg", ".jpeg"]:
            return "image/jpeg"
        elif ext == ".png":
            return "image/png"
        elif ext == ".webp":
            return "image/webp"
        elif ext == ".json":
            return "application/json"
        elif ext == ".onnx":
            return "application/octet-stream"

        mime_type, _ = mimetypes.guess_type(filepath)
        return mime_type or "application/octet-stream"

    def file_exists(self, file_key: str) -> bool:
        """Kiểm tra object đã tồn tại bằng head_object metadata"""
        try:
            self.client.head_object(Bucket=BUCKET_NAME, Key=file_key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            logger.error(f"Lỗi khi kiểm tra tồn tại của {file_key}: {e}")
            return False

    def upload_file(self, file_path: Path, file_key: str = None) -> bool:
        """Upload một file vật lý lên R2 (bỏ qua nếu đã có)"""
        if file_key is None:
            file_key = file_path.as_posix()

        # 1. KIỂM TRA TỒN TẠI
        if self.file_exists(file_key):
            logger.info(f"⏭️ Bỏ qua (Đã tồn tại): {file_key}")
            return True

        # 2. UPLOAD NẾU CHƯA CÓ
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
                        "Metadata": {"uploaded-by": self.metadata_tag},
                    },
                )
            logger.success(f"✅ Upload thành công: {file_key}")
            return True

        except ClientError as e:
            logger.error(f"❌ Lỗi khi upload {file_key}: {e}")
            return False


def process_directory(directory_name: str, uploader: R2Uploader):
    """Hàm tiện ích giúp quét và upload toàn bộ file trong một thư mục"""
    target_dir = Path(f"./{directory_name}")

    if not target_dir.exists() or not target_dir.is_dir():
        logger.error(
            f"Không tìm thấy thư mục '{directory_name}'. Vui lòng kiểm tra lại đường dẫn."
        )
        return

    files = [f for f in target_dir.iterdir() if f.is_file()]

    if not files:
        logger.warning(f"Thư mục '{directory_name}' trống. Không có gì để upload.")
        return

    logger.info(f"Tìm thấy {len(files)} file trong '{directory_name}' để xử lý.")

    success_count = 0
    fail_count = 0

    for file_path in files:
        if uploader.upload_file(file_path):
            success_count += 1
        else:
            fail_count += 1

    logger.info("-" * 40)
    logger.info(
        f"🎉 Hoàn tất '{directory_name}'! Thành công (gồm cả bỏ qua): {success_count} | Thất bại: {fail_count}"
    )
    logger.info("=" * 40)
