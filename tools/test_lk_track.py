import cv2
import numpy as np

cap = cv2.VideoCapture('data/remont_wc/oryginal.mp4')
frames = []
while True:
    ret, frame = cap.read()
    if not ret: break
    frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
cap.release()

pts_k5 = np.float32([
    [0, 96], [356, 176], [712, 176], # wall edge
    [200, 430], [430, 430], [430, 700], [200, 700] # bowl
]).reshape(-1, 1, 2)

k5_idx = 380
tracked_pts = {k5_idx: pts_k5}

curr_pts = pts_k5
for i in range(k5_idx - 1, -1, -1):
    next_pts, status, err = cv2.calcOpticalFlowPyrLK(frames[i+1], frames[i], curr_pts, None, winSize=(31,31), maxLevel=5)
    curr_pts = next_pts
    if i in [300, 200, 120, 10]:
        tracked_pts[i] = curr_pts

for k in [300, 200, 120, 10]:
    print(f"k{ {300:4, 200:3, 120:2, 10:1}[k] } (frame {k}):")
    print(tracked_pts[k].reshape(-1, 2))
