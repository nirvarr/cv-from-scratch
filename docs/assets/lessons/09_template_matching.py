"""
Module: Template Matching

Template matching finds a small image patch within a larger image. It slides the template around and computes a similarity score at each position. This is a simple but effective technique for object detection.
"""

import os
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from skimage import data

def get_images():
    """Gets a main image and extracts a template from it."""
    img = data.astronaut()
    # Convert to grayscale for simplicity
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Extract the astronaut's face as the template
    # Coordinates roughly found by inspecting the image
    template = img_gray[50:180, 150:280]
    return img_gray, template, img

def main():
    # 1. Setup
    img_gray, template, img_rgb = get_images()

    # 2. Process data
    # We use TM_CCOEFF_NORMED which is robust to lighting changes
    # It returns a correlation map (1.0 is perfect match, -1.0 is inverse)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    # Find the peak correlation
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # Extract top-left corner of the match
    top_left = max_loc

    # Get template dimensions
    h, w = template.shape
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # Draw a rectangle around the match on the original RGB image
    img_matched = img_rgb.copy()
    cv2.rectangle(img_matched, top_left, bottom_right, (255, 0, 0), 4)

    # 3. Visualization
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(template, cmap='gray')
    axes[0].set_title("Template to Find")
    axes[0].axis('off')

    # Show the correlation map. We add a marker at the max location.
    axes[1].imshow(res, cmap='viridis')
    axes[1].plot(max_loc[0], max_loc[1], 'rx', markersize=10, markeredgewidth=2)
    axes[1].set_title("Correlation Map\n(Red X marks peak)")
    axes[1].axis('off')

    axes[2].imshow(img_matched)
    axes[2].set_title("Detected Match")
    axes[2].axis('off')

    plt.tight_layout()
    os.makedirs('outputs', exist_ok=True)
    plt.savefig('outputs/09_template.png', dpi=100)
    plt.close(fig)

if __name__ == "__main__":
    np.random.seed(42)
    main()
