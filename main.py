import wave

from piper.voice import PiperVoice

model_path = "./models/vi_VN-vais1000-medium.onnx"
config_path = "./models/vi_VN-vais1000-medium.onnx.json"


model_path = "./models/banmai.onnx"
config_path = "./models/banmai.onnx.json"

voice = PiperVoice.load(model_path, config_path=config_path)


text = "Xin chào, đây là giọng đọc từ Piper TTS chạy trực tiếp trên Python."
output_file = "output.wav"

with wave.open(output_file, "wb") as wav_file:
    voice.synthesize_wav(text, wav_file)

print(f"Audio successfully saved to {output_file}")
