import cv2
import numpy as np

img = cv2.imread('data/remont_wc/kadry/k5.jpg')
h, w, _ = img.shape

# find the black button
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
best_btn = None
for c in contours:
    x,y,bw,bh = cv2.boundingRect(c)
    if 100 < bw < 400 and 50 < bh < 200 and y > 150 and y < 500 and 100 < x < 500:
        if best_btn is None or bw*bh > best_btn[2]*best_btn[3]:
            best_btn = (x, y, bw, bh)

if best_btn:
    print(f"Button: {best_btn[0]}, {best_btn[1]}, {best_btn[0]+best_btn[2]}, {best_btn[1]+best_btn[3]}")

# Let's find the green-to-white transition
# We can just print the argmax of the gradient in the Y direction for a few columns
col_left = 50
col_mid_l = int(w * 0.25)
col_mid_r = int(w * 0.75)

for col, name in [(20, "left_wall"), (200, "middle_left"), (600, "middle_right")]:
    # take a vertical slice in the upper part of the image
    slice_y = gray[0:400, col]
    # calculate gradient
    grad = np.abs(np.diff(slice_y.astype(np.float32)))
    max_y = np.argmax(grad)
    print(f"Transition at col {col} ({name}): y = {max_y}")

