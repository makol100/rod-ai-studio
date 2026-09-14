import cv2
import numpy as np

img = cv2.imread('data/remont_wc/kadry/k5.jpg')
h, w = img.shape[:2]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, 50, 150)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)

if lines is not None:
    vert_lines = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            if abs(x1 - x2) < 5:
                vert_lines.append((x1, y1, x2, y2))
                
    for l in sorted(vert_lines, key=lambda x: x[0]):
        if 20 < l[0] < w - 20:
            print(f"Vert line: x={l[0]}, y={l[1]} to {l[3]}")
