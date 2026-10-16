"""
Module: Convolution

Convolution is the process of sliding a small kernel over an image to apply effects. We will implement convolution from scratch in numpy. We'll compare our blur and sharpen kernels against OpenCV's optimized implementation.
"""

import os
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from skimage import data

def get_image():
    """Gets an image for convolution testing."""
    # Use camera man image
    img = data.camera()
    return img

def convolve2d_scratch(image, kernel):
    """
    Implements 2D convolution from scratch.
    Assumes a grayscale image and an odd-sized square kernel.
    """
    k_height, k_width = kernel.shape
    pad_h = k_height // 2
    pad_w = k_width // 2

    # Pad image to handle borders (zero padding)
    padded_img = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')

    # Output image
    output = np.zeros_like(image, dtype=np.float32)

    # Slide the kernel
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # Extract region
            region = padded_img[i:i+k_height, j:j+k_width]
            # Element-wise multiplication and sum
            output[i, j] = np.sum(region * kernel)

    return np.clip(output, 0, 255).astype(np.uint8)

def main():
    # 1. Setup
    img = get_image()

    # Define kernels
    # 5x5 Box Blur
    blur_kernel = np.ones((5, 5), np.float32) / 25.0

    # 3x3 Sharpen
    sharpen_kernel = np.array([
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0]
    ], dtype=np.float32)

    # 2. Process data
    # Run from scratch
    blur_scratch = convolve2d_scratch(img, blur_kernel)
    sharpen_scratch = convolve2d_scratch(img, sharpen_kernel)

    # Run OpenCV (for comparison in tests, but let's just show scratch here)
    # blur_cv2 = cv2.filter2D(img, -1, blur_kernel)

    # 3. Visualization
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(img, cmap='gray')
    axes[0].set_title("Original")
    axes[0].axis('off')

    axes[1].imshow(blur_scratch, cmap='gray')
    axes[1].set_title("Box Blur (Scratch)")
    axes[1].axis('off')

    axes[2].imshow(sharpen_scratch, cmap='gray')
    axes[2].set_title("Sharpen (Scratch)")
    axes[2].axis('off')

    plt.tight_layout()
    os.makedirs('outputs', exist_ok=True)
    plt.savefig('outputs/04_convolution.png', dpi=100)
    plt.close(fig)

if __name__ == "__main__":
    np.random.seed(42)
    main()
