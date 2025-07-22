import subprocess
import os

def extract_frames(filepath, fps=1, output_dir="static/frames"):
    """
    从视频中提取帧并保存为图片
    :param filepath: 视频文件路径
    :param fps: 提取帧的速率（每秒提取一帧）
    :param output_dir: 输出目录
    :return: 帧文件名列表
    """
    filename = os.path.basename(filepath)
    name, _ = os.path.splitext(filename)
    out_dir = os.path.join(output_dir, name)
    os.makedirs(out_dir, exist_ok=True)

    output_template = os.path.join(out_dir, "frame_%03d.jpg")

    cmd = [
        'ffmpeg',
        '-i', filepath,
        '-vf', f'fps={fps}',
        '-qscale:v', '2',   # 保证图像质量
        output_template
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg 抽帧失败: {result.stderr}")

    # 获取生成帧文件名
    frame_list = sorted([
        os.path.join(out_dir, f)
        for f in os.listdir(out_dir)
        if f.endswith('.jpg')
    ])

    return frame_list