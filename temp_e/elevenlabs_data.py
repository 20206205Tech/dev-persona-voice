import uuid
from dataclasses import dataclass

import elevenlabs_env


def generate_greeting_text(name: str, gender: str) -> str:
    gender_normalized = gender.strip().lower()

    if gender_normalized == "nam":
        pronoun = "tôi"
    elif gender_normalized == "nữ":
        pronoun = "mình"
    else:
        pronoun = "tôi"
    return f"Xin chào, {pronoun} là {name}. {pronoun.capitalize()} có thể giúp gì cho bạn về các vấn đề pháp luật?"


@dataclass
class DataEngine:
    id: uuid.UUID
    code: str
    name: str
    is_active: bool = True


@dataclass
class DataVoice:
    voice_uuid: uuid.UUID
    voice_code: str
    engine_id: uuid.UUID
    is_active: bool = True


@dataclass
class DataPersona:
    id: uuid.UUID
    name: str
    gender: str
    voice_uuid: uuid.UUID
    description: str
    avatar_url: str
    greeting_text: str
    greeting_audio_url: str
    is_active: bool = True


SAMPLE_ENGINE_DATA = []
SAMPLE_VOICE_DATA = []
SAMPLE_PERSONA_DATA = []


engine_edge = DataEngine(
    id=uuid.UUID("a12e3456-789a-bcde-f012-3456789abcde"),
    code="edge_tts",
    name="Edge TTS",
    is_active=True,
)
SAMPLE_ENGINE_DATA.append(engine_edge)

engine_elevenlabs = DataEngine(
    id=uuid.UUID("b12e3456-789a-bcde-f012-3456789abcde"),
    code="elevenlabs",
    name="ElevenLabs",
    is_active=True,
)
SAMPLE_ENGINE_DATA.append(engine_elevenlabs)


engine_piper = DataEngine(
    id=uuid.UUID("e12e3456-789a-bcde-f012-3456789abcde"),
    code="piper_tts",
    name="Piper TTS",
    is_active=True,
)
SAMPLE_ENGINE_DATA.append(engine_piper)


# 2. Tạo và append các đối tượng DataVoice (Sử dụng id từ đối tượng DataEngine đã tạo)
voice_nam_minh = DataVoice(
    voice_uuid=uuid.UUID("c12e3456-789a-bcde-f012-3456789abcde"),
    voice_code="vi-VN-NamMinhNeural",
    engine_id=engine_edge.id,
    is_active=True,
)
SAMPLE_VOICE_DATA.append(voice_nam_minh)

voice_hoai_my = DataVoice(
    voice_uuid=uuid.UUID("c12e3456-789a-bcde-f012-3456789abcd1"),
    voice_code="vi-VN-HoaiMyNeural",
    engine_id=engine_edge.id,
    is_active=True,
)
SAMPLE_VOICE_DATA.append(voice_hoai_my)

voice_quoc_hung = DataVoice(
    voice_uuid=uuid.UUID("c12e3456-789a-bcde-f012-3456789abcd2"),
    voice_code="IKne3meq5aSn9XLyUdCD",
    engine_id=engine_elevenlabs.id,
    is_active=True,
)
SAMPLE_VOICE_DATA.append(voice_quoc_hung)

voice_duc_kien = DataVoice(
    voice_uuid=uuid.UUID("c12e3456-789a-bcde-f012-3456789abcd3"),
    voice_code="pNInz6obpgDQGcFmaJgB",
    engine_id=engine_elevenlabs.id,
    is_active=True,
)
SAMPLE_VOICE_DATA.append(voice_duc_kien)

voice_lan_anh = DataVoice(
    voice_uuid=uuid.UUID("c12e3456-789a-bcde-f012-3456789abcd4"),
    voice_code="EXAVITQu4vr4xnSDxMaL",
    engine_id=engine_elevenlabs.id,
    is_active=True,
)
SAMPLE_VOICE_DATA.append(voice_lan_anh)

voice_thanh_truc = DataVoice(
    voice_uuid=uuid.UUID("c12e3456-789a-bcde-f012-3456789abcd5"),
    voice_code="hpp4J3VqNfWAUOO0d1Us",
    engine_id=engine_elevenlabs.id,
    is_active=True,
)
SAMPLE_VOICE_DATA.append(voice_thanh_truc)

voice_hung_dung = DataVoice(
    voice_uuid=uuid.UUID("c12e3456-789a-bcde-f012-3456789abcd6"),
    voice_code="cjVigY5qzO86Huf0OWal",
    engine_id=engine_elevenlabs.id,
    is_active=True,
)
SAMPLE_VOICE_DATA.append(voice_hung_dung)

SAMPLE_VOICE_DATA.extend(
    [
        DataVoice(
            voice_uuid=uuid.UUID("c12e3456-789a-bcde-f012-3456789abcd7"),
            voice_code="CwhRBWXzGAHq8TQ4Fs17",
            engine_id=engine_elevenlabs.id,
            is_active=True,
        ),
        DataVoice(
            voice_uuid=uuid.UUID("c12e3456-789a-bcde-f012-3456789abcd8"),
            voice_code="FGY2WhTYpPnrIDTdsKH5",
            engine_id=engine_elevenlabs.id,
            is_active=True,
        ),
        DataVoice(
            voice_uuid=uuid.UUID("c12e3456-789a-bcde-f012-3456789abcd9"),
            voice_code="Xb7hH8MSUJpSbSDYk0k2",
            engine_id=engine_elevenlabs.id,
            is_active=True,
        ),
        DataVoice(
            voice_uuid=uuid.UUID("c12e3456-789a-bcde-f012-3456789abcda"),
            voice_code="XrExE9yKIg1WjnnlVkGX",
            engine_id=engine_elevenlabs.id,
            is_active=True,
        ),
    ]
)


voice_ban_mai = DataVoice(
    voice_uuid=uuid.UUID("c12e3456-789a-bcde-f012-3456789abce0"),
    voice_code="banmai",
    engine_id=engine_piper.id,
    is_active=True,
)
SAMPLE_VOICE_DATA.append(voice_ban_mai)

voice_thanh_phuong = DataVoice(
    voice_uuid=uuid.UUID("c12e3456-789a-bcde-f012-3456789abce1"),
    voice_code="yannew",
    engine_id=engine_piper.id,
    is_active=True,
)
SAMPLE_VOICE_DATA.append(voice_thanh_phuong)

voice_minh_quang = DataVoice(
    voice_uuid=uuid.UUID("c12e3456-789a-bcde-f012-3456789abce2"),
    voice_code="minhquang",
    engine_id=engine_piper.id,
    is_active=True,
)
SAMPLE_VOICE_DATA.append(voice_minh_quang)

voice_manh_dung = DataVoice(
    voice_uuid=uuid.UUID("c12e3456-789a-bcde-f012-3456789abce3"),
    voice_code="duyoryx3175",
    engine_id=engine_piper.id,
    is_active=True,
)
SAMPLE_VOICE_DATA.append(voice_manh_dung)


# 3. Tạo và append các đối tượng DataPersona (Sử dụng voice_uuid của Voice)
persona_nam_minh = DataPersona(
    id=uuid.UUID("f0e747a0-48ee-4d60-9302-197a8e225673"),
    name="Nam Minh",
    gender="Nam",
    voice_uuid=voice_nam_minh.voice_uuid,
    description="Giọng nam miền Bắc trầm ấm, chững chạc.",
    avatar_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/images/vi-VN-NamMinhNeural-v1.png",
    greeting_text=generate_greeting_text("Nam Minh", "Nam"),
    greeting_audio_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/audio/vi-VN-NamMinhNeural.mp3",
    is_active=True,
)
SAMPLE_PERSONA_DATA.append(persona_nam_minh)

persona_hoai_my = DataPersona(
    id=uuid.UUID("d07e0f7a-07a5-4d7b-9abe-84d4fecaac59"),
    name="Hoài My",
    gender="Nữ",
    voice_uuid=voice_hoai_my.voice_uuid,
    description="Giọng nữ miền Nam nhẹ nhàng, truyền cảm.",
    avatar_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/images/vi-VN-HoaiMyNeural-v1.png",
    greeting_text=generate_greeting_text("Hoài My", "Nữ"),
    greeting_audio_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/audio/vi-VN-HoaiMyNeural.mp3",
    is_active=True,
)
SAMPLE_PERSONA_DATA.append(persona_hoai_my)

persona_quoc_hung = DataPersona(
    id=uuid.UUID("e6db7128-586e-4d19-b1ad-d9bb58aa0dee"),
    name="Quốc Hùng",
    gender="Nam",
    voice_uuid=voice_quoc_hung.voice_uuid,
    description="Giọng nam trầm ấm, tự tin và năng động.",
    avatar_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/images/20.jpg",
    greeting_text=generate_greeting_text("Quốc Hùng", "Nam"),
    greeting_audio_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/audio/IKne3meq5aSn9XLyUdCD.mp3",
    is_active=True,
)
SAMPLE_PERSONA_DATA.append(persona_quoc_hung)

persona_duc_kien = DataPersona(
    id=uuid.UUID("b1e9982f-b3ea-4c91-ba94-ca5e1666e4d7"),
    name="Đức Kiên",
    gender="Nam",
    voice_uuid=voice_duc_kien.voice_uuid,
    description="Giọng nam chững chạc, uy quyền và kiên định.",
    avatar_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/images/2.jpg",
    greeting_text=generate_greeting_text("Đức Kiên", "Nam"),
    greeting_audio_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/audio/pNInz6obpgDQGcFmaJgB.mp3",
    is_active=True,
)
SAMPLE_PERSONA_DATA.append(persona_duc_kien)

persona_lan_anh = DataPersona(
    id=uuid.UUID("02b6d3d3-6f70-4eb2-850d-f6e8e40bd3b9"),
    name="Lan Anh",
    gender="Nữ",
    voice_uuid=voice_lan_anh.voice_uuid,
    description="Giọng nữ trưởng thành, đáng tin cậy và tự tin.",
    avatar_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/images/47.jpg",
    greeting_text=generate_greeting_text("Lan Anh", "Nữ"),
    greeting_audio_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/audio/EXAVITQu4vr4xnSDxMaL.mp3",
    is_active=True,
)
SAMPLE_PERSONA_DATA.append(persona_lan_anh)


persona_thanh_truc = DataPersona(
    id=uuid.UUID("f6f3bf81-d5d8-44a1-9b5c-3bb3afb53c9d"),
    name="Thanh Trúc",
    gender="Nữ",
    voice_uuid=voice_thanh_truc.voice_uuid,
    description="Giọng nữ chuyên nghiệp, tươi sáng và ấm áp.",
    avatar_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/images/15.jpg",
    greeting_text=generate_greeting_text("Thanh Trúc", "Nữ"),
    greeting_audio_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/audio/hpp4J3VqNfWAUOO0d1Us.mp3",
    is_active=True,
)
SAMPLE_PERSONA_DATA.append(persona_thanh_truc)


persona_ban_mai = DataPersona(
    id=uuid.UUID("f0e747a0-48ee-4d60-9302-197a8e225680"),
    name="Ban Mai",
    gender="Nữ",
    voice_uuid=voice_ban_mai.voice_uuid,
    description="Giọng nữ nhẹ nhàng, trong trẻo.",
    avatar_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/images/26.jpg",
    greeting_text=generate_greeting_text("Ban Mai", "Nữ"),
    greeting_audio_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/audio/banmai.wav",
    is_active=True,
)
SAMPLE_PERSONA_DATA.append(persona_ban_mai)

persona_thanh_phuong = DataPersona(
    id=uuid.UUID("f0e747a0-48ee-4d60-9302-197a8e225681"),
    name="Thanh Phương",
    gender="Nữ",
    voice_uuid=voice_thanh_phuong.voice_uuid,
    description="Giọng nữ truyền cảm, ấm áp.",
    avatar_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/images/49.jpg",
    greeting_text=generate_greeting_text("Thanh Phương", "Nữ"),
    greeting_audio_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/audio/yannew.wav",
    is_active=True,
)
SAMPLE_PERSONA_DATA.append(persona_thanh_phuong)

persona_minh_quang = DataPersona(
    id=uuid.UUID("f0e747a0-48ee-4d60-9302-197a8e225682"),
    name="Minh Quang",
    gender="Nam",
    voice_uuid=voice_minh_quang.voice_uuid,
    description="Giọng nam trẻ trung, năng động.",
    avatar_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/images/39.jpg",
    greeting_text=generate_greeting_text("Minh Quang", "Nam"),
    greeting_audio_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/audio/minhquang.wav",
    is_active=True,
)
SAMPLE_PERSONA_DATA.append(persona_minh_quang)

persona_manh_dung = DataPersona(
    id=uuid.UUID("f0e747a0-48ee-4d60-9302-197a8e225683"),
    name="Mạnh Dũng",
    gender="Nam",
    voice_uuid=voice_manh_dung.voice_uuid,
    description="Giọng nam trầm ấm, vững chãi.",
    avatar_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/images/29.jpg",
    greeting_text=generate_greeting_text("Mạnh Dũng", "Nam"),
    greeting_audio_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/audio/duyoryx3175.wav",
    is_active=True,
)
SAMPLE_PERSONA_DATA.append(persona_manh_dung)


persona_hung_dung = DataPersona(
    id=uuid.UUID("f0e747a0-48ee-4d60-9302-197a8e225690"),
    name="Hùng Dũng",
    gender="Nam",
    voice_uuid=voice_hung_dung.voice_uuid,
    description="Giọng nam trầm ấm, truyền cảm.",
    avatar_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/images/79.jpg",
    greeting_text=generate_greeting_text("Hùng Dũng", "Nam"),
    greeting_audio_url=f"{elevenlabs_env.R2_PUBLIC_DOMAIN}/audio/cjVigY5qzO86Huf0OWal.mp3",
    is_active=True,
)
SAMPLE_PERSONA_DATA.append(persona_hung_dung)
