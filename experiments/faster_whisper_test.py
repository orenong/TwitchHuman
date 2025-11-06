from faster_whisper import WhisperModel

model_size = "small"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cpu", compute_type="float32")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe(r"C:\Users\oren166\Desktop\code\TheBestPerson-The-final-twitch-bot-project\danmanplayz_20251031_001138\segment_00034_20251031_001742.mp3", beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
