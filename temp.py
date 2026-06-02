# import boto3

# # Nạp cấu hình từ file env.py cùng thư mục
# import env

# # Cấu hình R2 - Lấy trực tiếp từ module env
# R2_ENDPOINT_URL = env.R2_ENDPOINT_URL
# R2_ACCESS_KEY_ID = env.R2_ACCESS_KEY_ID
# R2_SECRET_ACCESS_KEY = env.R2_SECRET_ACCESS_KEY

# # Tự động chọn Bucket dựa trên ENVIRONMENT
# BUCKET_NAME = "dev-persona" if env.ENVIRONMENT == "development" else "prod-persona"

# # Khởi tạo client R2 (Đã truyền các biến cấu hình vào đây)
# s3 = boto3.client(
#     "s3",
#     endpoint_url=R2_ENDPOINT_URL,
#     aws_access_key_id=R2_ACCESS_KEY_ID,
#     aws_secret_access_key=R2_SECRET_ACCESS_KEY,
#     region_name="auto",  # R2 sử dụng auto region
# )


# def cleanup_ongoing_uploads():
#     # Sử dụng BUCKET_NAME đã được tự động gán ở trên thay vì text cứng
#     response = s3.list_multipart_uploads(Bucket=BUCKET_NAME)

#     if "Uploads" in response:
#         print(
#             f"Tìm thấy {len(response['Uploads'])} upload đang bị treo trong bucket '{BUCKET_NAME}'. Bắt đầu dọn dẹp..."
#         )
#         for upload in response["Uploads"]:
#             upload_id = upload["UploadId"]
#             key = upload["Key"]
#             print(f"- Đang hủy: {key} (ID: {upload_id})")

#             # Lệnh hủy upload
#             s3.abort_multipart_upload(Bucket=BUCKET_NAME, Key=key, UploadId=upload_id)
#         print("✅ Đã dọn dẹp xong!")
#     else:
#         print(
#             f"✨ Không có multipart upload nào đang bị treo trong bucket '{BUCKET_NAME}'."
#         )


# if __name__ == "__main__":
#     cleanup_ongoing_uploads()
