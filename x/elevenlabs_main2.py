# import os
# import subprocess
# from dotenv import load_dotenv
# from elevenlabs.client import ElevenLabs

# # Nạp biến môi trường
# load_dotenv()

# # Khởi tạo client
# client = ElevenLabs(api_key=" ")

# # Danh sách các voice_id bạn muốn chạy
# voice_ids = [
    


#         "CwhRBWXzGAHq8TQ4Fs17",

#     "EXAVITQu4vr4xnSDxMaL",

#     "FGY2WhTYpPnrIDTdsKH5",

#     "IKne3meq5aSn9XLyUdCD",

#     "Xb7hH8MSUJpSbSDYk0k2",

#     "XrExE9yKIg1WjnnlVkGX",

#     "cjVigY5qzO86Huf0OWal",

#     "hpp4J3VqNfWAUOO0d1Us",

#     "pNInz6obpgDQGcFmaJgB",
 
# ]

# # Nội dung cần chuyển thành giọng nói
# text_content = "Xin chào bạn, hệ thống đã sẵn sàng."

# # Bắt đầu vòng lặp
# for v_id in voice_ids:
#     print(f"Đang xử lý voice_id: {v_id}...")

#     try:
#         file_name = f"{v_id}.mp3"

#         # Gọi API ElevenLabs
#         audio_generator = client.text_to_speech.convert(
#             text=text_content,
#             voice_id=v_id,
#             language_code="vi",
#             model_id="eleven_turbo_v2_5"
#         )

#         # Lưu file mp3 theo tên của voice_id
#         with open(file_name, "wb") as f:
#             for chunk in audio_generator:
#                 if chunk:
#                     f.write(chunk)

#         print(f"--- Đã lưu xong: {file_name}")

#         # Tùy chọn: Mở file ngay sau khi tải (Lưu ý: sẽ mở rất nhiều cửa sổ nếu danh sách dài)
#         subprocess.run(["start", file_name], shell=True)
#         import time
#         time.sleep(3)  # Tạm dừng 1 giây giữa các lần

#     except Exception as e:
#         print(f"Lỗi khi xử lý {v_id}: {e}")

# print("\nHoàn thành tất cả các giọng nói!")
