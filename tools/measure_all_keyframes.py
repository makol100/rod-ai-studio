import cv2
import numpy as np

for i in range(1, 6):
    img = cv2.imread(f'data/remont_wc/kadry/k{i}.jpg')
    if img is None:
        print(f"k{i}.jpg not found")
        continue
    h, w, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Find flush plate
    # Let's search for a black/dark rectangle in the image.
    # The flush plate is black, so it has low HSV Value (V < 60)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 60])
    mask = cv2.inRange(hsv, lower_black, upper_black)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    button_bbox = None
    for cnt in contours:
        x, y, bw, bh = cv2.boundingRect(cnt)
        area = bw * bh
        aspect = bw / bh if bh > 0 else 0
        # The button is usually between 5000 and 30000 px and aspect is ~1.4
        if 4000 < area < 40000 and 1.0 < aspect < 2.0:
            if button_bbox is None or area > (button_bbox[2] * button_bbox[3]):
                button_bbox = (x, y, bw, bh)
                
    # 2. Find green to white transition along columns
    # Green tiles have typical BGR where G is highest, B and R are lower, or overall it's a specific green shade.
    # Let's print out the average BGR values in a vertical stripe of width 10
    # to find where the green transitions to white/gray.
    # Green tiles in this WC typically have G > 100, B < 120, R < 120, and G > B + 10, G > R + 10.
    # White wall has higher values, usually B > 130, G > 130, R > 130 and very close to each other.
    # Let's scan columns 40, 200, 350, 550, 680 to find the first row from the top where it becomes GREEN (tiles)
    # or the last row from the bottom of white (transition).
    # Better yet, let's look at the color of the wall vs tiles.
    # Let's print the colors along columns to find the transition.
    
    print(f"\n--- k{i}.jpg ---")
    if button_bbox:
        print(f"Detected Button: x={button_bbox[0]}, y={button_bbox[1]}, w={button_bbox[2]}, h={button_bbox[3]} (area {button_bbox[2]*button_bbox[3]})")
    else:
        print("No button detected")
        
    for col_x in [40, 200, 350, 550, 680]:
        if col_x >= w: continue
        # Scan from y=0 to y=600, find the transition
        transition_y = None
        for y in range(5, 600):
            b, g, r = img[y, col_x].astype(float)
            # A good metric for green tiles: g - b > 5 and g - r > 5 and g > 60
            # A white wall is very bright and balanced: b > 140, g > 140, r > 140 and abs(b-g) < 15 and abs(g-r) < 15
            is_green = (g - b > 8) and (g - r > 8) and (g > 60)
            if is_green:
                transition_y = y
                break
        print(f"  Col x={col_x}: transition y = {transition_y}")
