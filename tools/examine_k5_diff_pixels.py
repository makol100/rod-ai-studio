import cv2
import numpy as np

img = cv2.imread('data/remont_wc/kadry/k5.jpg')

def find_jump(x, y_start, y_end):
    for y in range(y_start, y_end):
        v1 = np.mean(img[y, x])
        v2 = np.mean(img[y+1, x])
        if abs(v2 - v1) > 20: # threshold for jump
            return y
    return None

def find_exact(x, y_start, y_end, name):
    print(f"--- {name} (x={x}) ---")
    for y in range(y_start, y_end):
        print(f"y={y}: {img[y, x].tolist()} (avg {np.mean(img[y, x]):.1f})")

find_exact(40, 180, 210, "left_wall")
find_exact(200, 175, 195, "middle_left")
find_exact(550, 175, 195, "middle_right")

