import os
import subprocess
import whisper

def extract_audio(video_path, audio_path):
    cmd = ['ffmpeg', '-y', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', audio_path]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def generate_subtitles(video_path, output_dir="static/subtitles"):
    os.makedirs(output_dir, exist_ok=True)
    
    name, _ = os.path.splitext(os.path.basename(video_path))
    audio_path = os.path.join(output_dir, f"{name}.wav")
    srt_path = os.path.join(output_dir, f"{name}.srt")
    txt_path = os.path.join(output_dir, f"{name}.txt")

    # 1. 提取音频
    extract_audio(video_path, audio_path)

    # 2. Whisper识别
    model = whisper.load_model("base")  # 可选 tiny, base, small, medium, large
    result = model.transcribe(audio_path)

    # 3. 保存为 .srt
    with open(srt_path, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(result["segments"]):
            start = format_time(segment["start"])
            end = format_time(segment["end"])
            f.write(f"{i+1}\n{start} --> {end}\n{segment['text'].strip()}\n\n")

    # 4. 保存为纯文本
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(result['text'])

    return {
        "srt": srt_path,
        "txt": txt_path,
        "segments": result["segments"]
    }

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"