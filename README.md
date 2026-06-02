# Audio Transcriber

A simple local audio transcription tool using [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper) to convert `.wav` audio files into timestamped text transcripts.

This project was created to transcribe long audio recordings locally from the command line using Python.

## Features

- Transcribes `.wav` audio files locally
- Uses the `faster-whisper` implementation of OpenAI Whisper
- Outputs timestamped transcript lines
- Works well for long recordings, including 1-hour audio files
- Uses CPU by default
- No cloud API key required
- Keeps the audio file on your own machine

## Example Output

```text
Detected language: en with probability 1.00
[41.46s -> 49.76s] Hello. Hey, all good, thanks. Can you see me okay? Can you see me okay? Yes. Okay, that's good.
```

## Repository Structure

```text
audio-transcriber/
│
├── transcriber.py
├── transcript.txt
├── Recording 2.wav
└── README.md
```

> `transcript.txt` is generated after running the script.

## Requirements

- Python 3.10+
- Windows, macOS, or Linux
- Enough disk space for the Whisper model download
- Internet connection on first run to download the model from Hugging Face

The current script uses the `medium` Whisper model, which gives a good balance between accuracy and speed.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/audio-transcriber.git
cd audio-transcriber
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

On Windows:

```powershell
py -3.10 -m venv .venv
```

### 3. Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution with an error similar to:

```text
running scripts is disabled on this system
```

run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

Alternatively, use the current-session-only option:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\.venv\Scripts\Activate.ps1
```

### 4. Upgrade pip and Install Dependencies

```powershell
python -m pip install --upgrade pip setuptools wheel
pip install faster-whisper
```

## Usage

Place your `.wav` file in the root of the repository.

By default, the script expects the file to be called:

```text
Recording 2.wav
```

Run:

```powershell
python .\transcriber.py
```

The transcript will be printed to the console and saved to:

```text
transcript.txt
```

## Current Script

```python
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
```

## Notes on First Run

On the first run, `faster-whisper` will download the selected model from Hugging Face.

You may see warnings like:

```text
huggingface_hub cache-system uses symlinks by default
```

This is common on Windows. The transcription still works. The warning means the cache may use more disk space because Windows symlink support is not enabled.

You may also see:

```text
Warning: You are sending unauthenticated requests to the HF Hub.
```

This is also fine for normal usage. A Hugging Face token is only needed if you want higher download rate limits.

## Changing the Audio File

To transcribe a different file, change this line in `transcriber.py`:

```python
audio_file = "Recording 2.wav"
```

For example:

```python
audio_file = "meeting.wav"
```

## Choosing a Whisper Model

You can change the model here:

```python
model = WhisperModel("medium", device="cpu", compute_type="int8")
```

Common options:

| Model | Speed | Accuracy | Recommended Use |
|---|---:|---:|---|
| `tiny` | Very fast | Low | Quick rough tests |
| `base` | Fast | Basic | Simple audio |
| `small` | Good | Decent | Faster transcription |
| `medium` | Moderate | Good | Recommended default |
| `large-v3` | Slow | Best | Highest accuracy |

For most use cases, `medium` is a good default.

## CPU Configuration

The script is configured to run on CPU:

```python
device="cpu"
compute_type="int8"
```

This is slower than GPU transcription but works on most machines.

If you have a compatible NVIDIA GPU and CUDA installed, you can experiment with:

```python
model = WhisperModel("medium", device="cuda", compute_type="float16")
```

## Language Detection

The script currently assumes English:

```python
language="en"
```

If you want Whisper to auto-detect the language, remove that argument:

```python
segments, info = model.transcribe(
    audio_file,
    beam_size=5,
    vad_filter=True
)
```

## Voice Activity Detection

The script enables voice activity detection:

```python
vad_filter=True
```

This helps skip silence and non-speech sections, which is useful for long recordings.

## Output Format

The current output format is:

```text
[start_seconds -> end_seconds] transcribed text
```

Example:

```text
[41.46s -> 49.76s] Hello. Hey, all good, thanks. Can you see me okay?
```

## Optional: Generate Subtitle Files

You can extend the script to generate `.srt` subtitle files.

Example:

```python
from faster_whisper import WhisperModel

audio_file = "Recording 2.wav"

model = WhisperModel("medium", device="cpu", compute_type="int8")

segments, info = model.transcribe(
    audio_file,
    beam_size=5,
    vad_filter=True,
    language="en"
)

segments = list(segments)

def format_timestamp(seconds: float) -> str:
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

with open("transcript.txt", "w", encoding="utf-8") as txt:
    for segment in segments:
        txt.write(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text.strip()}\n")

with open("transcript.srt", "w", encoding="utf-8") as srt:
    for index, segment in enumerate(segments, start=1):
        srt.write(f"{index}\n")
        srt.write(f"{format_timestamp(segment.start)} --> {format_timestamp(segment.end)}\n")
        srt.write(f"{segment.text.strip()}\n\n")
```

## Troubleshooting

### PowerShell script execution is disabled

If you see:

```text
Activate.ps1 cannot be loaded because running scripts is disabled on this system
```

run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### `onnxruntime_test.exe` installation error on Windows

If package installation fails with an error involving:

```text
onnxruntime_test.exe
```

use a clean virtual environment instead of installing packages globally:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install --no-cache-dir faster-whisper
```

### Hugging Face symlink warning

If you see:

```text
huggingface_hub cache-system uses symlinks by default
```

the program can still run correctly.

To remove the warning, either enable Windows Developer Mode or run Python as administrator.

You can also suppress the warning with:

```powershell
$env:HF_HUB_DISABLE_SYMLINKS_WARNING="1"
```

### Slow transcription

Transcription speed depends on:

- Audio length
- CPU performance
- Selected Whisper model
- Whether GPU acceleration is available

For faster transcription, try:

```python
model = WhisperModel("small", device="cpu", compute_type="int8")
```

For better accuracy, try:

```python
model = WhisperModel("large-v3", device="cpu", compute_type="int8")
```

## Recommended `.gitignore`

Add a `.gitignore` file to avoid committing virtual environments, large audio files, and generated transcripts:

```gitignore
# Python
__pycache__/
*.pyc

# Virtual environment
.venv/
venv/

# Generated transcripts
transcript.txt
transcript.srt

# Audio files
*.wav
*.mp3
*.m4a
*.aac
*.flac

# IDE files
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db
```

## Recommended `requirements.txt`

```text
faster-whisper
```

## Privacy

This project runs transcription locally. The audio file itself is not sent to a transcription API.

However, on the first run, the Whisper model is downloaded from Hugging Face.

## Limitations

- Speaker names are not identified automatically.
- The current script does not perform speaker diarisation.
- Very noisy audio may produce lower-quality transcripts.
- CPU transcription can be slow for large models.
- The default script currently handles one file at a time.

## Future Improvements

Potential improvements:

- Add command-line arguments for audio filename
- Generate `.srt` subtitles by default
- Support batch transcription of multiple files
- Add `.mp3`, `.m4a`, and `.flac` examples
- Add speaker diarisation
- Add automatic summary generation
- Add meeting notes and action-item extraction
- Add optional GPU support instructions
- Package as a small CLI tool

## Licence

MIT Licence.
