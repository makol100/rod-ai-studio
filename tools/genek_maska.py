import cv2
import numpy as np
import os

# Keyframes (true measured bounding boxes for the flush plate)
k_frames = {
    10: (591, 483, 121, 69),
    120: (14, 981, 170, 157),
    200: (621, 720, 91, 114),
    300: (267, 160, 151, 118),
    380: (249, 264, 140, 99),
}

def get_polys(plate):
    px, py, pw, ph = plate
    
    # Wall y
    wall_y = int(py - 0.88 * ph)
    
    # Bowl
    bx1 = int(px + pw/2 - 0.8 * pw)
    bx2 = int(px + pw/2 + 0.8 * pw)
    by1 = int(py + ph + 0.6 * ph)
    by2 = int(py + ph + 3.0 * ph) # 45cm above floor approx
    
    # Return as list of points for polygon
    wall_poly = np.array([[-2000, -2000], [3000, -2000], [3000, wall_y], [-2000, wall_y]], dtype=np.float32)
    bowl_poly = np.array([[bx1, by1], [bx2, by1], [bx2, by2], [bx1, by2]], dtype=np.float32)
    
    return wall_poly, bowl_poly

# Read all frames
cap = cv2.VideoCapture('data/remont_wc/oryginal.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

frames = []
while True:
    ret, frame = cap.read()
    if not ret: break
    frames.append(frame)
cap.release()

# Calculate homographies between consecutive frames
# H_seq[i] will be homography from frame i to i+1
H_seq = []
for i in range(len(frames)-1):
    gray1 = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frames[i+1], cv2.COLOR_BGR2GRAY)
    
    pts1 = cv2.goodFeaturesToTrack(gray1, maxCorners=200, qualityLevel=0.01, minDistance=30)
    if pts1 is not None:
        pts2, status, err = cv2.calcOpticalFlowPyrLK(gray1, gray2, pts1, None, winSize=(21,21), maxLevel=3)
        good1 = pts1[status == 1]
        good2 = pts2[status == 1]
        
        if len(good1) >= 4:
            H, _ = cv2.findHomography(good1, good2, cv2.RANSAC, 3.0)
        else:
            H = np.eye(3)
    else:
        H = np.eye(3)
        
    if H is None:
        H = np.eye(3)
        
    H_seq.append(H)

# Function to get accumulated homography from frame A to frame B
def get_H_A_to_B(A, B):
    H = np.eye(3)
    if A < B:
        for i in range(A, B):
            H = H_seq[i] @ H
    elif A > B:
        for i in range(A-1, B-1, -1):
            H = np.linalg.inv(H_seq[i]) @ H
    return H

out_mask = cv2.VideoWriter('data/remont_wc/maska.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height), isColor=False)
out_preview = cv2.VideoWriter('data/remont_wc/maska_podglad.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

keys = sorted(list(k_frames.keys()))

for i in range(len(frames)):
    # Find the closest keyframes
    if i <= keys[0]:
        k_left = keys[0]
        k_right = keys[0]
    elif i >= keys[-1]:
        k_left = keys[-1]
        k_right = keys[-1]
    else:
        for j in range(len(keys)-1):
            if keys[j] <= i <= keys[j+1]:
                k_left = keys[j]
                k_right = keys[j+1]
                break
                
    # Transform polygons
    if k_left == k_right:
        H = get_H_A_to_B(k_left, i)
        w_poly, b_poly = get_polys(k_frames[k_left])
        w_poly = cv2.perspectiveTransform(w_poly.reshape(-1, 1, 2), H)
        b_poly = cv2.perspectiveTransform(b_poly.reshape(-1, 1, 2), H)
    else:
        # Blend points from left and right
        w_poly_l, b_poly_l = get_polys(k_frames[k_left])
        w_poly_r, b_poly_r = get_polys(k_frames[k_right])
        
        H_l = get_H_A_to_B(k_left, i)
        H_r = get_H_A_to_B(k_right, i)
        
        w_poly_l = cv2.perspectiveTransform(w_poly_l.reshape(-1, 1, 2), H_l).reshape(-1, 2)
        b_poly_l = cv2.perspectiveTransform(b_poly_l.reshape(-1, 1, 2), H_l).reshape(-1, 2)
        
        w_poly_r = cv2.perspectiveTransform(w_poly_r.reshape(-1, 1, 2), H_r).reshape(-1, 2)
        b_poly_r = cv2.perspectiveTransform(b_poly_r.reshape(-1, 1, 2), H_r).reshape(-1, 2)
        
        t = (i - k_left) / (k_right - k_left)
        w_poly = (1 - t) * w_poly_l + t * w_poly_r
        b_poly = (1 - t) * b_poly_l + t * b_poly_r
        
        w_poly = w_poly.reshape(-1, 1, 2)
        b_poly = b_poly.reshape(-1, 1, 2)

    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.fillPoly(mask, [np.int32(w_poly)], 255)
    cv2.fillPoly(mask, [np.int32(b_poly)], 255)
    
    out_mask.write(mask)
    
    colored_mask = np.zeros_like(frames[i])
    colored_mask[:,:,2] = mask
    preview = cv2.addWeighted(frames[i], 0.7, colored_mask, 0.3, 0)
    out_preview.write(preview)

out_mask.release()
out_preview.release()
print("KROK 1: Maska OpenCV wykonana pomyslnie.")
