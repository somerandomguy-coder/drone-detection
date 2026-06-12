from os import environ

import cv2
import dotenv
import numpy as np
from ultralytics import YOLO

dotenv.load_dotenv()
MODEL_PATH = environ.get("model_path", "models/yolov8m.pt")
SAVE_OUTPUT = bool(environ.get("save_output", False))
CONFIDENCE = float(environ.get("confidence", 0.5))
IMAGE_SIZE = int(environ.get("image_size", 640))

print(
    f"Model configuration:\nmodel_path: {MODEL_PATH},\nsave_output: {SAVE_OUTPUT},\nconfidence: {CONFIDENCE},\nimage_size: {IMAGE_SIZE}"
)


def get_yolo():
    yolo = YOLO(MODEL_PATH)
    return yolo


async def model(yolo, input_path):
    print(f"model from {MODEL_PATH} predict image from {input_path}")
    if input_path is None:
        return []
    image = cv2.imread(input_path)

    if image is None:
        return []

    results = yolo.predict(
        source=input_path, save=SAVE_OUTPUT, conf=CONFIDENCE, imgsz=IMAGE_SIZE
    )

    result = results[0]
    output = []

    if result.boxes is None:
        return []

    for box in result.boxes:
        xywh = box.xywh[0].tolist()
        conf = box.conf[0].item()
        result = {"coordinate": xywh, "confidence": conf}
        output.append(result)

    return output
