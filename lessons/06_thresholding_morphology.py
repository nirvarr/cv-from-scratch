"""
Module: Thresholding and Morphology

Thresholding turns a grayscale image into a binary mask. Morphological operations like erosion and dilation help clean up noise in these masks. We can combine them into opening and closing operations for robust region selection.
"""

import os
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_synthetic_document():
    """Creates a synthetic image resembling text with uneven lighting."""
    img = np.full((300, 400), 200, dtype=np.uint8)

    # Add some text
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, "Computer Vision", (20, 100), font, 1.5, (50,), 3)
    cv2.putText(img, "Thresholding", (50, 180), font, 1.2, (30,), 2)

    # Add uneven lighting (gradient)
    gradient = np.zeros_like(img, dtype=float)
    for i in range(img.shape[1]):
        gradient[:, i] = i / img.shape[1] * 100

    img = cv2.add(img, gradient.astype(np.uint8))

    # Add some salt and pepper noise
    noise = np.random.randint(0, 255, img.shape)
    img[noise > 240] = 255
    img[noise < 10] = 0

    return img

def main():
    # 1. Setup
    img = create_synthetic_document()

    # 2. Process data - Thresholding
    # Global thresholding
    _, thresh_global = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Otsu's thresholding
    _, thresh_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Adaptive thresholding (handles uneven lighting)
    thresh_adaptive = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 21, 10)

    # 3. Process data - Morphology
    # Let's use the adaptive threshold result and invert it so text is white
    mask = cv2.bitwise_not(thresh_adaptive)

    kernel = np.ones((3,3), np.uint8)

    # Erode: shrinks white regions, removes small noise
    eroded = cv2.erode(mask, kernel, iterations=1)

    # Dilate: expands white regions, fills small holes
    dilated = cv2.dilate(mask, kernel, iterations=1)

    # Opening: Erode followed by Dilate (removes small noise)
    opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Closing: Dilate followed by Erode (fills small holes inside objects)
    closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # 4. Visualization
    # Thresholding Figure
    fig1, axes1 = plt.subplots(2, 2, figsize=(10, 8))

    axes1[0, 0].imshow(img, cmap='gray')
    axes1[0, 0].set_title("Original (Uneven Light + Noise)")
    axes1[0, 0].axis('off')

    axes1[0, 1].imshow(thresh_global, cmap='gray')
    axes1[0, 1].set_title("Global Threshold (v=127)")
    axes1[0, 1].axis('off')

    axes1[1, 0].imshow(thresh_otsu, cmap='gray')
    axes1[1, 0].set_title("Otsu's Threshold")
    axes1[1, 0].axis('off')

    axes1[1, 1].imshow(thresh_adaptive, cmap='gray')
    axes1[1, 1].set_title("Adaptive Threshold")
    axes1[1, 1].axis('off')

    plt.tight_layout()
    os.makedirs('outputs', exist_ok=True)
    fig1.savefig('outputs/06_thresholding.png', dpi=100)
    plt.close(fig1)

    # Morphology Figure
    fig2, axes2 = plt.subplots(2, 2, figsize=(10, 8))

    axes2[0, 0].imshow(mask, cmap='gray')
    axes2[0, 0].set_title("Binary Mask (Inverted Adaptive)")
    axes2[0, 0].axis('off')

    axes2[0, 1].imshow(opened, cmap='gray')
    axes2[0, 1].set_title("Opening (Removes background noise)")
    axes2[0, 1].axis('off')

    axes2[1, 0].imshow(eroded, cmap='gray')
    axes2[1, 0].set_title("Erosion")
    axes2[1, 0].axis('off')

    axes2[1, 1].imshow(closed, cmap='gray')
    axes2[1, 1].set_title("Closing (Fills holes in text)")
    axes2[1, 1].axis('off')

    plt.tight_layout()
    fig2.savefig('outputs/06_morphology.png', dpi=100)
    plt.close(fig2)

if __name__ == "__main__":
    np.random.seed(42)
    main()
