import cv2
import numpy as np

img = cv2.imread('data/remont_wc/kadry/k5.jpg')
patch = img[250:380, 230:410]
gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)
contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

print("Contours in patch (250:380, 230:410):")
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if w > 20 and h > 20:
        print(f"x={x+230}, y={y+250}, w={w}, h={h}")
