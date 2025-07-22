import subprocess
import json

def get_video_info(filepath):
    cmd = [
        '/Users/zb/anaconda3/bin/ffprobe',
        '-v', 'error',
        '-print_format', 'json',
        '-show_streams',
        '-show_format',
        filepath
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"ffprobe error:{result.stderr}")
    info = json.loads(result.stdout)

    video_info = {
        "duration": float(info["format"]["duration"]),
        "bit_rate": int(info["format"]["bit_rate"]),
    }

    for stream in info["streams"]:
        if stream["codec_type"] == "video":
            video_info["width"] = stream["width"]
            video_info["height"] = stream["height"]
            video_info["video_codec"] = stream["codec_name"]
            video_info["frame_rate"] = eval(stream["r_frame_rate"])
        elif stream["codec_type"] == "audio":
            video_info["audio_codec"] = stream["codec_name"]

    return video_info