from os import environ

import cv2
import dotenv
import numpy as np
import yaml
from ultralytics import YOLO

dotenv.load_dotenv()
MODEL_PATH = environ.get("model_path", "meomoe")
SAVE_OUTPUT = environ.get("save_output", False)
CONFIDENCE = environ.get("confidence", 0.5)
IMAGE_SIZE = environ.get("image_size", 640)

print(
    f"Model configuration:\nmodel_path: {MODEL_PATH},\nsave_output: {SAVE_OUTPUT},\nconfidence: {CONFIDENCE},\nimage_size: {IMAGE_SIZE}"
)


def getYolo(path):
    yolo = YOLO(path)
    return yolo


def model(input_path):
    print(f"model from {MODEL_PATH} predict image from {input_path}")
    if input_path is None:
        return []
    image = cv2.imread(input_path)

    if image is None:
        return []

    yolo = getYolo(MODEL_PATH)

    result = yolo.predict(source=input_path, save=True, conf=0.5, imgsz=640)

    return result
