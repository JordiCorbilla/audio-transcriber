from faster_whisper import WhisperModel

audio_file = "Recording 2.wav"

# Good CPU default:
model = WhisperModel("medium", device="cpu", compute_type="int8")

segments, info = model.transcribe(
    audio_file,
    beam_size=5,
    vad_filter=True,
    language="en"  # remove or change if not English
)

print(f"Detected language: {info.language} with probability {info.language_probability:.2f}")

with open("transcript.txt", "w", encoding="utf-8") as f:
    for segment in segments:
        line = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text.strip()}"
        print(line)
        f.write(line + "\n")