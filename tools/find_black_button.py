import cv2
import numpy as np
import sys
import glob

def find_button(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return "brak"
    
    # Convert to HSV to find black
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Define range for black color
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 60])
    
    # Threshold the HSV image to get only black colors
    mask = cv2.inRange(hsv, lower_black, upper_black)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    candidates = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        aspect = w / h if h > 0 else 0
        
        # Flush button heuristic: somewhat rectangular, area between some bounds
        if 500 < area < 50000 and 0.5 < aspect < 4.0:
            candidates.append((area, x, y, w, h))
            
    if not candidates:
        return "brak"
        
    candidates.sort(reverse=True)
    # Return the largest black candidate
    _, x, y, w, h = candidates[0]
    return f"x={x}, y={y}, w={w}, h={h}"

for file in sorted(glob.glob('data/remont_wc/kadry/k*.jpg')):
    print(f"{file}: {find_button(file)}")
