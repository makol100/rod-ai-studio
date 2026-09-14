import cv2
import numpy as np

cap = cv2.VideoCapture('data/remont_wc/oryginal.mp4')
frames = []
while True:
    ret, frame = cap.read()
    if not ret: break
    frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
cap.release()

orb = cv2.ORB_create(3000)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

kps = []
dess = []
for f in frames:
    kp, des = orb.detectAndCompute(f, None)
    kps.append(kp)
    dess.append(des)

k5_idx = 380

H_accum = np.eye(3)
Hs = {k5_idx: H_accum.copy()}

# Track backward
for i in range(k5_idx - 1, -1, -1):
    matches = bf.match(dess[i+1], dess[i])
    matches = sorted(matches, key=lambda x: x.distance)
    
    if len(matches) < 10:
        print(f"Backward frame {i}: Not enough matches")
        break
        
    src_pts = np.float32([kps[i+1][m.queryIdx].pt for m in matches[:100]]).reshape(-1, 1, 2)
    dst_pts = np.float32([kps[i][m.trainIdx].pt for m in matches[:100]]).reshape(-1, 1, 2)
    
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    if H is not None:
        H_accum = H @ H_accum
    Hs[i] = H_accum.copy()

# Track forward
H_accum = np.eye(3)
for i in range(k5_idx + 1, len(frames)):
    matches = bf.match(dess[i-1], dess[i])
    matches = sorted(matches, key=lambda x: x.distance)
    
    if len(matches) < 10:
        print(f"Forward frame {i}: Not enough matches")
        break
        
    src_pts = np.float32([kps[i-1][m.queryIdx].pt for m in matches[:100]]).reshape(-1, 1, 2)
    dst_pts = np.float32([kps[i][m.trainIdx].pt for m in matches[:100]]).reshape(-1, 1, 2)
    
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    if H is not None:
        H_accum = H @ H_accum
    Hs[i] = H_accum.copy()

pts_k5 = np.float32([
    [356, 176], # Top center edge of tiles in k5
    [249, 264]  # Top left of flush plate in k5
]).reshape(-1, 1, 2)

for k in [300, 200, 120, 10]:
    if k in Hs:
        mapped = cv2.perspectiveTransform(pts_k5, Hs[k])
        print(f"Frame {k}: {mapped.reshape(-1, 2)}")
