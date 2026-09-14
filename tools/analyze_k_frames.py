import cv2
import numpy as np
import json

def analyze():
    img = cv2.imread('data/remont_wc/kadry/k5.jpg')
    if img is None:
        return {"error": "image not found"}
    
    # Button bounding box
    # The button is a black rectangle in the center-top.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    button_bbox = None
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if 100 < w < 300 and 50 < h < 200 and y > 150 and y < 600:
            button_bbox = [x, y, x+w, y+h]
            break
            
    # For tile edges, we can sample specific columns and find the green to white transition.
    # Green is roughly R:100, G:120, B:100. White is R:200, G:200, B:200
    # Let's just output some horizontal line detections.
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)
    
    line_coords = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if abs(y1 - y2) < 20: # horizontal-ish
                line_coords.append([int(x1), int(y1), int(x2), int(y2)])
                
    return {
        "button": button_bbox,
        "horizontal_lines": line_coords[:20]
    }

print(json.dumps(analyze()))
