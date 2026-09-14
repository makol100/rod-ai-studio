import cv2
import numpy as np

img = cv2.imread('data/remont_wc/kadry/k5.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)

contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    area = w * h
    # A flush button is usually somewhat rectangular, fairly large. Let's say area between 5000 and 100000 pixels.
    if 10000 < area < 150000 and 1.0 < w/h < 3.0:
        print(f"Candidate: x={x}, y={y}, w={w}, h={h}, area={area}, aspect={w/h:.2f}")
