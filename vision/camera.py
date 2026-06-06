import cv2
import os
from datetime import datetime

def capture_image(output_dir: str = "images"):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if not ret:
        return None

    filename = os.path.join(output_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
    cv2.imwrite(filename, frame)

    cap.release()
    return filename