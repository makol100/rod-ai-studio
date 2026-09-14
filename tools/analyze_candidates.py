import cv2
import numpy as np

img = cv2.imread('data/remont_wc/kadry/k5.jpg')

candidates = [
    (230, 1044, 307, 236),
    (404, 947, 199, 151),
    (94, 928, 185, 173),
    (110, 866, 160, 140),
    (122, 814, 142, 115),
    (133, 770, 120, 92),
    (234, 639, 186, 96),
    (248, 263, 142, 101)
]

for x, y, w, h in candidates:
    patch = img[y:y+h, x:x+w]
    avg_color = np.mean(patch, axis=(0,1))
    std_color = np.std(patch, axis=(0,1))
    print(f"Rect (x={x}, y={y}, w={w}, h={h}): Avg color BGR={avg_color.astype(int)}, Std={std_color.astype(int)}")
