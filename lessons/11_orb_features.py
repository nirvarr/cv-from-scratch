"""
Module: Feature Detection and Matching

ORB is a fast algorithm for detecting and describing keypoints in an image. These descriptions can be used to match features across different images. This forms the basis for tasks like image stitching and tracking.
"""

import os
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from skimage import data

def get_images():
    """Gets an image and creates a transformed version to match against."""
    img1 = data.astronaut()
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)

    # Create a transformed version (rotated, scaled, and translated)
    rows, cols = img1_gray.shape
    M = cv2.getRotationMatrix2D((cols/2, rows/2), 30, 0.8)
    M[0, 2] += 50 # Translate X
    M[1, 2] -= 30 # Translate Y

    img2_gray = cv2.warpAffine(img1_gray, M, (cols, rows))

    return img1_gray, img2_gray

def main():
    # 1. Setup
    img1, img2 = get_images()

    # 2. Process data
    # Initialize ORB detector
    orb = cv2.ORB_create(nfeatures=500)

    # Find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # Create BFMatcher (Brute Force Matcher) object
    # ORB uses binary descriptors, so we use HAMMING distance
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    matches = bf.match(des1, des2)

    # Sort them in the order of their distance
    matches = sorted(matches, key=lambda x: x.distance)

    # Draw first 50 matches
    img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None,
                                  flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # 3. Visualization
    fig, axes = plt.subplots(1, 1, figsize=(15, 8))

    axes.imshow(img_matches)
    axes.set_title("ORB Feature Matching (Top 50 Matches)")
    axes.axis('off')

    plt.tight_layout()
    os.makedirs('outputs', exist_ok=True)
    plt.savefig('outputs/11_orb.png', dpi=100)
    plt.close(fig)

if __name__ == "__main__":
    np.random.seed(42)
    main()
