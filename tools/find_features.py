import cv2
import numpy as np
import sys

def find_flush_plate(img_path):
    img = cv2.imread(img_path)
    if img is None:
        print(f"Cannot read {img_path}")
        return
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Black color mask
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])
    mask = cv2.inRange(hsv, lower_black, upper_black)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    candidates = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        # Flush plate is likely a rectangle, not too small, not too large
        if 5000 < area < 50000 and 0.5 < w/h < 2.0:
            candidates.append((x, y, w, h, area))
            
    # Sort by area descending
    candidates.sort(key=lambda x: x[4], reverse=True)
    if candidates:
        print(f"Flush plate candidates in {img_path}: {candidates[:3]}")
    else:
        print(f"No flush plate found in {img_path}")

find_flush_plate('data/remont_wc/kadry/k1.jpg')
find_flush_plate('data/remont_wc/kadry/k5.jpg')
