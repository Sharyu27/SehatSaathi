import cv2

def compare_images(img1_path, img2_path):
    img1 = cv2.imread(img1_path, 0)
    img2 = cv2.imread(img2_path, 0)

    if img1 is None or img2 is None:
        return False

    # Make comparison robust to different resolutions.
    target_size = (256, 256)
    img1 = cv2.resize(img1, target_size, interpolation=cv2.INTER_AREA)
    img2 = cv2.resize(img2, target_size, interpolation=cv2.INTER_AREA)

    diff = cv2.absdiff(img1, img2)
    score = diff.sum()

    # Lower score means more similar. Tune threshold per lighting/camera.
    return score < 2_500_000