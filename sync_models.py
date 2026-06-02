from loguru import logger

from r2_uploader import R2Uploader, process_directory


def main():
    logger.info("🚀 BẮT ĐẦU ĐỒNG BỘ AI MODELS")

    # Xử lý thư mục models
    model_uploader = R2Uploader(metadata_tag="model-sync-script")
    process_directory("models", model_uploader)


if __name__ == "__main__":
    main()
