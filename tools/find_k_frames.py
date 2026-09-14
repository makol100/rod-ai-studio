import cv2
import os
import numpy as np

def find_frame_indices(video_path, frames_dir):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Could not open video")
        return
    
    k_images = {}
    for i in range(1, 6):
        img = cv2.imread(os.path.join(frames_dir, f'k{i}.jpg'), cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (128, 256))
        k_images[f'k{i}'] = img
        
    best_matches = {k: {"idx": -1, "diff": float('inf')} for k in k_images}
    
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_resized = cv2.resize(frame_gray, (128, 256))
        
        for k, k_img in k_images.items():
            diff = np.mean(np.abs(frame_resized.astype(np.float32) - k_img.astype(np.float32)))
            if diff < best_matches[k]["diff"]:
                best_matches[k]["diff"] = diff
                best_matches[k]["idx"] = idx
                
        idx += 1
        
    cap.release()
    for k, v in best_matches.items():
        print(f"{k}: frame {v['idx']} (diff {v['diff']:.2f})")

find_frame_indices('data/remont_wc/oryginal.mp4', 'data/remont_wc/kadry')
