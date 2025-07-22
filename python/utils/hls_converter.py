import os
import subprocess

def convert_to_hls(input_video_path, output_dir="static/hls", segment_time=10):
    os.makedirs(output_dir, exist_ok=True)

    name, _ = os.path.splitext(os.path.basename(input_video_path))
    hls_path = os.path.join(output_dir, name)
    os.makedirs(hls_path, exist_ok=True)

    m3u8_path = os.path.join(hls_path, f"{name}.m3u8")

    cmd = [
        "ffmpeg",
        "-i", input_video_path,
        "-codec:", "copy",
        "-start_number", "0",
        "-hls_time", str(segment_time),
        "-hls_list_size", "0",
        "-f", "hls",
        m3u8_path
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"HLS 转换失败: {result.stderr}")

    return m3u8_path