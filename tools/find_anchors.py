import cv2
import numpy as np

img5 = cv2.imread('data/remont_wc/kadry/k5.jpg', cv2.IMREAD_GRAYSCALE)
orb = cv2.ORB_create(5000)
kp5, des5 = orb.detectAndCompute(img5, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

pts_k5 = np.float32([
    [0, 176], [356, 176], [712, 176], # wall
    [249, 264], [249+140, 264+99], # flush plate
    [200, 430], [430, 430], [430, 700], [200, 700] # bowl
]).reshape(-1, 1, 2)

for i in range(1, 6):
    img = cv2.imread(f'data/remont_wc/kadry/k{i}.jpg', cv2.IMREAD_GRAYSCALE)
    kp, des = orb.detectAndCompute(img, None)
    matches = bf.match(des5, des)
    matches = sorted(matches, key=lambda x: x.distance)
    
    src_pts = np.float32([kp5[m.queryIdx].pt for m in matches[:100]]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp[m.trainIdx].pt for m in matches[:100]]).reshape(-1, 1, 2)
    
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    if H is not None:
        mapped = cv2.perspectiveTransform(pts_k5, H).reshape(-1, 2)
        print(f"k{i} anchors:")
        print(f"  Wall: {mapped[:3].astype(int).tolist()}")
        print(f"  Flush: {mapped[3:5].astype(int).tolist()}")
        print(f"  Bowl: {mapped[5:].astype(int).tolist()}")
    else:
        print(f"k{i} homography failed")
