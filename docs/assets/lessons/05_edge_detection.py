"""
Module: Edge Detection

Edges occur where pixel intensities change rapidly. We will build a Sobel edge detector from scratch to compute image gradients. Then, we will explore the powerful Canny edge detection algorithm.
"""

import os
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from skimage import data

def get_image():
    # Use coins for edge detection
    return data.coins()

def sobel_scratch(image):
    """Implements Sobel edge detection using OpenCV's filter2D for the convolution part."""
    # Define Sobel kernels
    Kx = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]], dtype=np.float32)

    Ky = np.array([[-1, -2, -1],
                   [ 0,  0,  0],
                   [ 1,  2,  1]], dtype=np.float32)

    # Apply convolution (we use cv2.filter2D here as we built convolve from scratch in lesson 4)
    # Using float32 output to capture negative gradients
    Ix = cv2.filter2D(image.astype(np.float32), cv2.CV_32F, Kx)
    Iy = cv2.filter2D(image.astype(np.float32), cv2.CV_32F, Ky)

    # Compute gradient magnitude
    magnitude = np.sqrt(Ix**2 + Iy**2)
    # Normalize to 0-255
    magnitude = (magnitude / magnitude.max() * 255).astype(np.uint8)

    return Ix, Iy, magnitude

def main():
    # 1. Setup
    img = get_image()

    # 2. Process data
    # Sobel
    Ix, Iy, sobel_mag = sobel_scratch(img)

    # Canny (using OpenCV)
    # Canny needs a blurred image for best results, though it does some internally
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    canny_edges = cv2.Canny(blurred, 100, 200)

    # 3. Visualization
    # Sobel Figure
    fig1, axes1 = plt.subplots(1, 3, figsize=(15, 5))

    axes1[0].imshow(img, cmap='gray')
    axes1[0].set_title("Original")
    axes1[0].axis('off')

    # Show X gradient
    axes1[1].imshow(Ix, cmap='gray')
    axes1[1].set_title("Sobel X Gradient")
    axes1[1].axis('off')

    axes1[2].imshow(sobel_mag, cmap='gray')
    axes1[2].set_title("Sobel Magnitude")
    axes1[2].axis('off')

    plt.tight_layout()
    os.makedirs('outputs', exist_ok=True)
    fig1.savefig('outputs/05_sobel.png', dpi=100)
    plt.close(fig1)

    # Canny Figure
    fig2, axes2 = plt.subplots(1, 2, figsize=(10, 5))

    axes2[0].imshow(img, cmap='gray')
    axes2[0].set_title("Original")
    axes2[0].axis('off')

    axes2[1].imshow(canny_edges, cmap='gray')
    axes2[1].set_title("Canny Edges")
    axes2[1].axis('off')

    plt.tight_layout()
    fig2.savefig('outputs/05_canny.png', dpi=100)
    plt.close(fig2)

if __name__ == "__main__":
    np.random.seed(42)
    main()
