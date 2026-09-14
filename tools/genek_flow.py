import cv2
import numpy as np

k_frames = {
    10: (591, 483, 121, 69),
    120: (14, 981, 170, 157),
    # 200 is omitted because we don't know the exact position, let optical flow track it!
    300: (270, 148, 151, 118),
    380: (249, 264, 140, 99),
}

# Actually we can just track from 380 backward to 0, and correct at keyframes!
# Let's do dense points on the plate
