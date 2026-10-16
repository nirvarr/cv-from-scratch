"""
Module: Color Spaces

RGB is not the only way to represent color. Color spaces like HSV and LAB separate color information from brightness. This makes color-based object segmentation much more robust.
"""

import os
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from skimage import data

def get_image():
    """Gets an image from skimage data."""
    # Use the famous 'astronaut' image which has a clear red patch on the uniform
    img = data.astronaut()
    return img

def segment_red_hsv(img_rgb):
    """Segments red colors using HSV space."""
    # Convert RGB to HSV
    # In OpenCV, it expects BGR normally, but we can do RGB to HSV directly
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)

    # Red in HSV wraps around 0 and 180 (OpenCV uses 0-179 for H)
    # Lower red
    lower_red_1 = np.array([0, 70, 50])
    upper_red_1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red_1, upper_red_1)

    # Upper red
    lower_red_2 = np.array([170, 70, 50])
    upper_red_2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(img_hsv, lower_red_2, upper_red_2)

    # Combine masks
    mask = mask1 | mask2

    # Apply mask
    result = cv2.bitwise_and(img_rgb, img_rgb, mask=mask)
    return img_hsv, mask, result

def main():
    # 1. Setup
    img_rgb = get_image()

    # 2. Process data
    img_hsv, mask, segmented = segment_red_hsv(img_rgb)

    # 3. Visualization 1: Color spaces
    fig1, axes1 = plt.subplots(1, 3, figsize=(12, 4))

    axes1[0].imshow(img_rgb)
    axes1[0].set_title("Original (RGB)")
    axes1[0].axis('off')

    # Show Hue channel (colored using a colormap for visualization)
    axes1[1].imshow(img_hsv[:, :, 0], cmap='hsv')
    axes1[1].set_title("Hue Channel (H)")
    axes1[1].axis('off')

    # Show Saturation channel
    axes1[2].imshow(img_hsv[:, :, 1], cmap='gray')
    axes1[2].set_title("Saturation Channel (S)")
    axes1[2].axis('off')

    plt.tight_layout()
    os.makedirs('outputs', exist_ok=True)
    fig1.savefig('outputs/02_color_spaces.png', dpi=100)
    plt.close(fig1)

    # 3. Visualization 2: Segmentation
    fig2, axes2 = plt.subplots(1, 3, figsize=(12, 4))

    axes2[0].imshow(img_rgb)
    axes2[0].set_title("Original Image")
    axes2[0].axis('off')

    axes2[1].imshow(mask, cmap='gray')
    axes2[1].set_title("Red Color Mask")
    axes2[1].axis('off')

    axes2[2].imshow(segmented)
    axes2[2].set_title("Segmented Result")
    axes2[2].axis('off')

    plt.tight_layout()
    fig2.savefig('outputs/02_segmentation.png', dpi=100)
    plt.close(fig2)

if __name__ == "__main__":
    np.random.seed(42)
    main()
