import cv2
import numpy as np

def to_ascii(img, width=60):
    if img is None or img.size == 0: return ""
    h, w = img.shape[:2]
    aspect_ratio = h / w
    new_h = int(aspect_ratio * width * 0.55)
    resized = cv2.resize(img, (width, new_h))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    chars = " .:-=+*#%@"
    ascii_str = ""
    for y in range(new_h):
        for x in range(width):
            ascii_str += chars[gray[y, x] // 32]
        ascii_str += "\n"
    return ascii_str

def find_buttons(img_path):
    img = cv2.imread(img_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 60])
    mask = cv2.inRange(hsv, lower_black, upper_black)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    candidates = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        aspect = w / h if h > 0 else 0
        if 200 < area < 50000 and 0.5 < aspect < 5.0:
            candidates.append((area, x, y, w, h))
    
    candidates.sort(reverse=True)
    print(f"=== {img_path} ===")
    for idx, (area, x, y, w, h) in enumerate(candidates[:3]):
        print(f"Candidate {idx}: x={x}, y={y}, w={w}, h={h}, area={area}")
        crop = img[y:y+h, x:x+w]
        print(to_ascii(crop, 40))

for i in range(1, 6):
    find_buttons(f'data/remont_wc/kadry/k{i}.jpg')
