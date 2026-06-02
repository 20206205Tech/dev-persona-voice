import os

import requests


def download_images():
    # Tên thư mục để lưu ảnh (lưu ở thư mục hiện tại)
    save_dir = "images"

    # Tạo thư mục nếu nó chưa tồn tại
    os.makedirs(save_dir, exist_ok=True)

    # URL gốc với {} để điền số thứ tự vào
    base_url = "https://mockmind-api.uifaces.co/content/human/{}.jpg"

    # Dựa theo danh sách của bạn, ảnh chạy từ 1 đến 222
    for i in range(1, 223):
        url = base_url.format(i)
        file_name = f"{i}.jpg"
        file_path = os.path.join(save_dir, file_name)

        try:
            # Gửi request để tải ảnh
            response = requests.get(url, stream=True)

            # Kiểm tra xem ảnh có tồn tại trên server không (status_code == 200)
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Đã tải thành công: {file_name}")
            else:
                print(
                    f"Không tìm thấy hoặc lỗi {response.status_code} tại: {file_name}"
                )

        except Exception as e:
            print(f"Lỗi kết nối khi tải {file_name}: {e}")


if __name__ == "__main__":
    download_images()
