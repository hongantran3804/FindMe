import cv2
import numpy as np
from drawDetection import draw_detection_boxes

from ultralytics import YOLO  # type: ignore

model = YOLO("yolov8n.pt", "v8")

image_path = "./images/img0.JPG"
image = cv2.imread(image_path)

detection_output = model.predict(source=image_path, conf=0.25, save=False)
boxes = detection_output[0].boxes.data.numpy()

with open("./utils/coco.txt", "r") as f:
    classes = f.read().splitlines()



draw_detection_boxes(image, boxes, classes)


