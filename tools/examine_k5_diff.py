import cv2
import numpy as np

img = cv2.imread('data/remont_wc/kadry/k5.jpg')

for name, x in [("left_wall (x=40)", 40), ("middle_left (x=200)", 200), ("middle_right (x=550)", 550), ("right_wall (x=680)", 680)]:
    print(f"--- {name} ---")
    for y in range(100, 250, 10):
        print(f"y={y}: {img[y, x].tolist()}")

