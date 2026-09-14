import cv2
import numpy as np

for i in range(1, 6):
    img = cv2.imread(f'data/remont_wc/kadry/k{i}.jpg')
    if img is None:
        print(f"k{i}.jpg not found")
        continue
    h, w, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    print(f"\n--- k{i}.jpg ({w}x{h}) ---")
    # Let's check gradient peaks in the upper half of the image at columns:
    # x = 50, 150, 250, 350, 450, 550, 650
    cols = [20, 100, 200, 350, 500, 600, 690]
    transitions = []
    for col in cols:
        if col >= w:
            continue
        # We search for the tile-wall boundary which is typically a dark line (shadow/grout) 
        # or color transition. Let's look at gradient of gray.
        slice_y = gray[0:500, col]
        grad = np.abs(np.diff(slice_y.astype(np.float32)))
        # Filter peaks
        peaks = np.where(grad > 15)[0]
        # Let's print the top 3 peaks for this column
        sorted_peaks = sorted(peaks, key=lambda p: grad[p], reverse=True)
        transitions.append(f"x={col}: {sorted_peaks[:3]}")
    print("Peaks:", ", ".join(transitions))
