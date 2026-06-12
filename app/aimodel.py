from os import environ

import cv2
import dotenv
import numpy as np
from ultralytics import YOLO

dotenv.load_dotenv()
MODEL_PATH = environ.get("model_path", "models/yolov8m.pt")
SAVE_OUTPUT = environ.get("save_output", False)
CONFIDENCE = environ.get("confidence", 0.5)
IMAGE_SIZE = environ.get("image_size", 640)

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

    result = yolo.predict(
        source=input_path, save=SAVE_OUTPUT, conf=CONFIDENCE, imgsz=IMAGE_SIZE
    )

    return result
