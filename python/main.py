"""
视频处理服务主应用

提供视频上传、视频信息提取和视频抽帧功能的Flask后端服务
"""
# 导入Flask框架及请求处理相关模块
from flask import Flask,request,jsonify
# 导入werkzeug工具函数，用于安全处理文件名
from werkzeug.utils import secure_filename
# 导入操作系统接口模块，用于文件路径处理
import os
from utils.video_info import get_video_info
from utils.frame_extractor import extract_frames
from utils.transcoder import transcode_video
from utils.subtitle_generator import generate_subtitles
from utils.frame_extractor import extract_frames_ffmpeg
from utils.yolo_detector import detect_objects_yolo
from utils.hls_converter import convert_to_hls

app = Flask(__name__)
# 配置文件上传目录
app.config['UPLOAD_FOLDER'] = 'uploads'  # 视频文件存储路径
# 视频上传模块
# 视频上传API端点
# 支持POST方法，接收multipart/form-data格式的视频文件
@app.route('/upload', methods=['POST'])
def upload_file():
    """
    处理视频文件上传

    请求方式: POST
    请求体: multipart/form-data格式，包含名为'file'的视频文件
    返回: JSON格式响应，包含上传状态和文件信息
    """
    # 验证请求中是否包含文件数据
    if 'file' not in request.files:
# 统一响应格式: code(状态码), message(提示信息), data(业务数据)
        return jsonify({"code": 400, "message": "没有文件被上传"})
    file = request.files['file']
    # 验证文件名是否为空
    if file.filename == '':
        return jsonify({"code": 400, "message": "文件名为空"})

    # 使用werkzeug的secure_filename函数清理文件名，防止路径遍历攻击
    filename = secure_filename(file.filename)
    # 确保上传目录存在
    # 确保上传目录存在，exist_ok=True避免目录已存在时抛出异常
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    # 构造完整的文件保存路径
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        file.save(save_path)
        return jsonify({
            "code": 200,
            "message": "上传成功",
            "data": {
                "filename": filename,
                "save_path": save_path
            }
        })
    except Exception as e:
        return jsonify({"code": 500, "message": f"文件保存失败: {str(e)}"})

# 视频信息查询API端点
# 支持GET方法，通过URL参数filename指定视频文件
@app.route('/video/info', methods=['GET'])
def video_info():
    """
    获取视频文件信息

    请求方式: GET
    请求参数: filename - 视频文件名
    返回: JSON格式响应，包含视频时长、比特率、分辨率等信息
    """
    # 从URL查询参数中获取视频文件名
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"code": 400, "message": "缺少 filename 参数"})

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # 验证文件是否存在
    if not os.path.exists(filepath):
        return jsonify({"code": 404, "message": "文件不存在"})

    try:
        # 调用视频信息提取工具，获取视频元数据
        info = get_video_info(filepath)
        return jsonify({"code": 200, "message": "ok", "data": info})
    # 捕获视频信息提取过程中的异常并返回错误信息
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})

# 视频抽帧API端点
# 支持POST方法，接收JSON格式的请求参数
@app.route('/video/extract-frames', methods=['POST'])
def extract_video_frames():
    """
    从视频中提取帧图像

    请求方式: POST
    请求体: JSON格式，包含filename(视频文件名)和fps(抽帧速率，可选，默认1)
    返回: JSON格式响应，包含抽帧结果和帧文件路径列表
    """
    # 解析JSON格式的请求体数据
    data = request.get_json()
    filename = data.get('filename')
    fps = data.get('fps', 1)

    if not filename:
        return jsonify({"code": 400, "message": "缺少 filename"})

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({"code": 404, "message": "视频文件不存在"})

    try:
        # 调用帧提取工具，按指定帧率从视频中提取帧图像
        frame_files = extract_frames(filepath, fps=fps)
        return jsonify({
            "code": 200,
            "message": "抽帧成功",
            "data": {
                "frames": frame_files
            }
        })
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": str(e)
        })

@app.route('/video/transcode', methods=['POST'])
def transcode():
    data = request.get_json()
    filename = data.get("filename")
    video_codec = data.get("video_codec", "libx264")
    audio_codec = data.get("audio_codec", "aac")
    bitrate = data.get("bitrate", "1000k")
    resolution = data.get("resolution", "1280x720")

    if not filename:
        return jsonify({"code": 400, "message": "缺少 filename"})

    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(input_path):
        return jsonify({"code": 404, "message": "视频文件不存在"})

    try:
        output_path = transcode_video(
            input_path=input_path,
            video_codec=video_codec,
            audio_codec=audio_codec,
            bitrate=bitrate,
            resolution=resolution
        )
        return jsonify({
            "code": 200,
            "message": "转码成功",
            "data": {
                "output_file": output_path
            }
        })
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": str(e)
        })
'''
字幕识别API端点
支持POST方法，接收JSON格式的请求参数
请求方式: POST
请求体: JSON格式，包含filename(视频文件名)
返回: JSON格式响应，包含字幕文件路径、纯文本文件路径和字幕段落列表
'''
@app.route('/video/subtitles', methods=['POST'])
def subtitles():
    data = request.get_json()
    filename = data.get("filename")
    if not filename:
        return jsonify({"code": 400, "message": "缺少 filename"})

    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(video_path):
        return jsonify({"code": 404, "message": "文件不存在"})

    try:
        result = generate_subtitles(video_path)
        return jsonify({
            "code": 200,
            "message": "字幕识别成功",
            "data": {
                "srt_file": result["srt"],
                "txt_file": result["txt"],
                "segments": result["segments"]
            }
        })
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})
'''
YOLO 检测API端点
支持POST方法，接收JSON格式的请求参数
请求方式: POST
请求体: JSON格式，包含filename(视频文件名)、fps(抽帧速率，可选，默认1)、model(模型名称，可选，默认yolov8n.pt)
返回: JSON格式响应，包含检测结果
'''
@app.route('/video/yolo-detect', methods=['POST'])
def yolo_detect():
    data = request.get_json()
    filename = data.get("filename")
    fps = data.get("fps", 1)
    model_name = data.get("model", "yolov8n.pt")

    if not filename:
        return jsonify({"code": 400, "message": "缺少 filename"})

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({"code": 404, "message": "视频不存在"})

    try:
        # 1. 抽帧
        frame_paths = extract_frames_ffmpeg(filepath, fps=fps)

        # 2. YOLO 检测
        result = detect_objects_yolo(frame_paths, model_name=model_name)

        return jsonify({
            "code": 200,
            "message": "检测完成",
            "data": result
        })
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": str(e)
        })
'''
HLS 切片API端点
支持POST方法，接收JSON格式的请求参数
请求方式: POST
请求体: JSON格式，包含filename(视频文件名)、segment_time(切片时间，可选，默认10秒)
返回: JSON格式响应，包含HLS切片后的m3u8文件路径
'''
@app.route('/video/hls', methods=['POST'])
def convert_hls():
    data = request.get_json()
    filename = data.get("filename")
    segment_time = int(data.get("segment_time", 10))

    if not filename:
        return jsonify({"code": 400, "message": "缺少 filename"})

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({"code": 404, "message": "视频不存在"})

    try:
        m3u8_path = convert_to_hls(filepath, segment_time=segment_time)
        return jsonify({
            "code": 200,
            "message": "HLS 切片完成",
            "data": {
                "m3u8_url": m3u8_path
            }
        })
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": str(e)
        })

if __name__ == '__main__':
    # 启动Flask开发服务器
    # debug=True启用自动重载，port=5000指定服务端口
    app.run(debug=True, port=5000)