import os

# Keep your Fedora/Wayland fix at the top
os.environ["QT_QPA_PLATFORM"] = "xcb"

import cv2
from ultralytics import YOLO

video_source = "./examples/fixed_drone_easiest.mp4"  # could be some youtube url

if not os.path.exists(video_source):
    print("Path doesn't exist, download a video or change the source to new url/path")
    exit(1)

# 1. Load the model
model = YOLO("./models/best.pt")

# 2. Choose tracker
tracker = "botsort.yaml"
# tracker = "bytetrack.yaml"

# 3. Track object from video and save result
results = model.track(
    source=video_source,
    save=True,
    tracker=tracker,
    conf=0.25,
    imgsz=640,
    persist=True,
    stream=True,
)

print("--------------------------------------------------")
print("Processing video background... Saving to runs/detect/track/")
print("--------------------------------------------------")

# 4. Efficiently consume the generator to let YOLO process and save the video
frame_count = 0
for r in results:
    frame_count += 1
    # Print progress every 30 frames so you know it's working
    if frame_count % 30 == 0:
        print(f"Processed {frame_count} frames...")

print("--------------------------------------------------")
print("SUCCESS: Processing finished!")
print(
    "Look in your project directory under: runs/detect/track/ exp/ (or track2, track3, etc.)"
)
print("--------------------------------------------------")
