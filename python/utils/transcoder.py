import os
import subprocess

def transcode_video(
    input_path,
    output_dir="static/transcoded",
    video_codec="libx264",
    audio_codec="aac",
    bitrate="1000k",
    resolution="1280x720"
):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(input_path)
    name, _ = os.path.splitext(filename)
    output_path = os.path.join(output_dir, f"{name}_transcoded.mp4")

    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", video_codec,
        "-c:a", audio_codec,
        "-b:v", bitrate,
        "-s", resolution,
        output_path
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"转码失败: {result.stderr}")

    return output_path