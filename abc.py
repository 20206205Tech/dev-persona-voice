import asyncio
import os
import edge_tts

# Định nghĩa dữ liệu các câu chào
PERSONA_GREETINGS = [
    {
        "name": "Nam Minh",
        "voice_id": "vi-VN-NamMinhNeural",
        "text": "Xin chào, tôi là Nam Minh. Tôi có thể giúp gì cho bạn về các vấn đề pháp luật?",
        "output_path": "audio/greeting_nam_minh.mp3"
    },
    {
        "name": "Hoài My",
        "voice_id": "vi-VN-HoaiMyNeural",
        "text": "Chào bạn, mình là Hoài My. Mình có thể giúp gì cho bạn về các vấn đề pháp luật?",
        "output_path": "audio/greeting_hoai_my.mp3"
    }
]

async def generate_greeting_audios():
    # Đảm bảo thư mục audio tồn tại
    os.makedirs("audio", exist_ok=True)
    
    for persona in PERSONA_GREETINGS:
        print(f"⏳ Đang tạo audio cho {persona['name']} ({persona['voice_id']})...")
        
        # Khởi tạo giao tiếp với edge-tts
        communicate = edge_tts.Communicate(text=persona["text"], voice=persona["voice_id"])
        
        # Lưu trực tiếp luồng âm thanh ra file
        await communicate.save(persona["output_path"])
        
        print(f"✅ Đã lưu thành công: {persona['output_path']}\n")

if __name__ == "__main__":
    # Chạy vòng lặp sự kiện bất đồng bộ
    asyncio.run(generate_greeting_audios())