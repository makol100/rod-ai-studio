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
    [0, 96], [356, 176], [712, 176],
    [200, 430], [430, 430], [430, 700], [200, 700]
]).reshape(-1, 1, 2)

curr_pts = pts_k5.copy()
orb = cv2.ORB_create(5000)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

k5_idx = 380

# Keep track of keypoints
kps = []
dess = []
for f in frames:
    kp, des = orb.detectAndCompute(f, None)
    kps.append(kp)
    dess.append(des)

tracked_pts = {k5_idx: curr_pts.copy()}

for i in range(k5_idx - 1, -1, -1):
    matches = bf.match(dess[i+1], dess[i])
    matches = sorted(matches, key=lambda x: x.distance)
    
    if len(matches) < 10:
        print(f"Frame {i}: Not enough matches")
        break
        
    src_pts = np.float32([kps[i+1][m.queryIdx].pt for m in matches[:150]]).reshape(-1, 1, 2)
    dst_pts = np.float32([kps[i][m.trainIdx].pt for m in matches[:150]]).reshape(-1, 1, 2)
    
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    if H is not None:
        curr_pts = cv2.perspectiveTransform(curr_pts, H)
    
    if i in [300, 200, 120, 10]:
        tracked_pts[i] = curr_pts.copy()

for k in [300, 200, 120, 10]:
    if k in tracked_pts:
        print(f"k{ {300:4, 200:3, 120:2, 10:1}[k] } (frame {k}):")
        print(tracked_pts[k].reshape(-1, 2))
