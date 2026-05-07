import cv2

def capture_image(path: str) -> bool:
    cam = cv2.VideoCapture(0)

    success, frame = cam.read()

    if success:
        cv2.imwrite(path, frame)

    cam.release()
    return success