from loguru import logger

from r2_uploader import R2Uploader, process_directory


def main():
    logger.info("🚀 BẮT ĐẦU ĐỒNG BỘ MEDIA (AVATARS & EDGE TTS)")

    # Xử lý thư mục avatars
    avatar_uploader = R2Uploader(metadata_tag="avatar-sync-script")
    process_directory("avatars", avatar_uploader)

    # Xử lý thư mục edge_tts
    tts_uploader = R2Uploader(metadata_tag="edge-tts-sync-script")
    process_directory("edge_tts", tts_uploader)


if __name__ == "__main__":
    main()
