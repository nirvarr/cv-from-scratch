"""
Module: Contours and Shape Measurements

Contours trace the outlines of objects in binary images. Connected components labeling helps separate and identify distinct regions. We can compute simple shape properties like area and perimeter from these components.
"""

import os
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_shapes_image():
    """Creates a binary image with distinct shapes."""
    img = np.zeros((300, 400), dtype=np.uint8)

    # Draw a circle
    cv2.circle(img, (100, 100), 50, 255, -1)

    # Draw a rectangle
    cv2.rectangle(img, (200, 50), (350, 150), 255, -1)

    # Draw a polygon (triangle)
    pts = np.array([[100, 200], [50, 280], [150, 280]], np.int32)
    cv2.fillPoly(img, [pts], 255)

    # Add a hole in the rectangle
    cv2.circle(img, (275, 100), 20, 0, -1)

    return img

def main():
    # 1. Setup
    img = create_shapes_image()

    # 2. Process data
    # Find contours
    # RETR_TREE retrieves all contours and creates a full family hierarchy list
    # CHAIN_APPROX_SIMPLE compresses horizontal, vertical, and diagonal segments
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Create an RGB image to draw on
    output_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    # Draw contours (in green)
    cv2.drawContours(output_img, contours, -1, (0, 255, 0), 2)

    # Measure shapes and draw text
    for i, contour in enumerate(contours):
        # Calculate area
        area = cv2.contourArea(contour)

        # Calculate perimeter (True means closed contour)
        perimeter = cv2.arcLength(contour, True)

        # Calculate moments to find the center (centroid)
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # Put text near the centroid
            # Filter out the hole contour for cleaner text
            if area > 1000:
                cv2.putText(output_img, f"A:{int(area)}", (cX - 30, cY),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Connected Components
    # 8-way connectivity
    num_labels, labels = cv2.connectedComponents(img, connectivity=8)

    # Map labels to colors for visualization
    label_hue = np.uint8(179 * labels / np.max(labels))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

    # Convert HSV to RGB
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2RGB)

    # Set background (label 0) to black
    labeled_img[label_hue == 0] = 0

    # 3. Visualization
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(img, cmap='gray')
    axes[0].set_title("Original Binary Image")
    axes[0].axis('off')

    axes[1].imshow(output_img)
    axes[1].set_title(f"Contours & Area ({len(contours)} contours found)")
    axes[1].axis('off')

    axes[2].imshow(labeled_img)
    axes[2].set_title(f"Connected Components ({num_labels-1} objects)")
    axes[2].axis('off')

    plt.tight_layout()
    os.makedirs('outputs', exist_ok=True)
    plt.savefig('outputs/07_contours.png', dpi=100)
    plt.close(fig)

if __name__ == "__main__":
    np.random.seed(42)
    main()
