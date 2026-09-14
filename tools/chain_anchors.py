import cv2
import numpy as np

pts_k5 = np.float32([
    [0, 176], [356, 176], [712, 176], # wall
    [249, 264], [389, 363], # flush plate
    [200, 430], [430, 430], [430, 700], [200, 700] # bowl
]).reshape(-1, 1, 2)

anchors = {5: pts_k5.copy()}

orb = cv2.ORB_create(5000)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

for i in range(4, 0, -1):
    img1 = cv2.imread(f'data/remont_wc/kadry/k{i+1}.jpg', cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(f'data/remont_wc/kadry/k{i}.jpg', cv2.IMREAD_GRAYSCALE)
    
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches[:100]]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches[:100]]).reshape(-1, 1, 2)
    
    H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    anchors[i] = cv2.perspectiveTransform(anchors[i+1], H)

for i in range(1, 6):
    mapped = anchors[i].reshape(-1, 2)
    print(f"k{i} anchors:")
    print(f"  Wall: {mapped[:3].astype(int).tolist()}")
    print(f"  Flush: {mapped[3:5].astype(int).tolist()}")
    print(f"  Bowl: {mapped[5:].astype(int).tolist()}")
