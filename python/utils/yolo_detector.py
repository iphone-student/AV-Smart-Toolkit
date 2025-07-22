import os
from ultralytics import YOLO
import cv2

def detect_objects_yolo(frame_paths, model_name='yolov8n.pt', conf_thres=0.3):
    model = YOLO(model_name)  # 模型可选 yolov8n.pt, yolov5s.pt 等

    results = []
    for frame_path in frame_paths:
        image = cv2.imread(frame_path)
        if image is None:
            continue

        detect_result = model.predict(image, conf=conf_thres, verbose=False)[0]

        frame_detections = []
        for box in detect_result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(float, box.xyxy[0])
            label = model.names[cls_id]
            frame_detections.append({
                "label": label,
                "confidence": round(conf, 2),
                "bbox": [x1, y1, x2, y2]
            })

        results.append({
            "frame": frame_path,
            "objects": frame_detections
        })

    return results
