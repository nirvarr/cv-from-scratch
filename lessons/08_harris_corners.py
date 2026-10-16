"""
Module: Harris Corner Detection

Corners are image features that vary significantly in all directions. The Harris corner detector identifies these points using local gradients. We will implement this algorithm completely from scratch.
"""

import os
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_checkerboard():
    """Creates a simple checkerboard pattern."""
    img = np.zeros((200, 200), dtype=np.uint8)
    square_size = 50
    for i in range(0, 200, square_size):
        for j in range(0, 200, square_size):
            if (i // square_size + j // square_size) % 2 == 0:
                img[i:i+square_size, j:j+square_size] = 255
    return img

def harris_corners_scratch(img, window_size=3, k=0.04, threshold_ratio=0.01):
    """Implements Harris corner detection from scratch."""
    # 1. Calculate image gradients Ix and Iy using Sobel
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    Ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)

    Ix = cv2.filter2D(img.astype(np.float32), -1, Kx)
    Iy = cv2.filter2D(img.astype(np.float32), -1, Ky)

    # 2. Calculate products of derivatives (Ixx, Iyy, Ixy)
    Ixx = Ix ** 2
    Iyy = Iy ** 2
    Ixy = Ix * Iy

    # 3. Sum of products of derivatives (windowing)
    # Using a uniform window (box filter) for simplicity, though Gaussian is better
    kernel = np.ones((window_size, window_size), np.float32)
    Sxx = cv2.filter2D(Ixx, -1, kernel)
    Syy = cv2.filter2D(Iyy, -1, kernel)
    Sxy = cv2.filter2D(Ixy, -1, kernel)

    # 4. Define the matrix M(x,y) = [[Sxx, Sxy], [Sxy, Syy]]
    # Calculate response function R = det(M) - k(trace(M))^2
    det = (Sxx * Syy) - (Sxy ** 2)
    trace = Sxx + Syy
    R = det - k * (trace ** 2)

    # 5. Thresholding
    threshold = threshold_ratio * R.max()
    corner_image = np.zeros_like(R, dtype=np.uint8)
    corner_image[R > threshold] = 255

    # Extract coordinates of corners
    corners = np.argwhere(R > threshold)

    return R, corner_image, corners

def main():
    # 1. Setup
    img = create_checkerboard()

    # 2. Process data
    R, corner_image, corners = harris_corners_scratch(img)

    # OpenCV implementation for comparison
    # Block size 3, aperture 3 for Sobel, k=0.04
    dst = cv2.cornerHarris(img.astype(np.float32), 3, 3, 0.04)
    dst_norm = np.empty(dst.shape, dtype=np.float32)
    cv2.normalize(dst, dst_norm, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    dst_norm_scaled = cv2.convertScaleAbs(dst_norm)

    cv_corner_img = np.zeros_like(img)
    cv_corner_img[dst_norm_scaled > 100] = 255

    # Create visual output
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    for y, x in corners:
        # Draw red circles at detected corners
        cv2.circle(img_color, (x, y), 3, (255, 0, 0), -1)

    # 3. Visualization
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))

    axes[0].imshow(img, cmap='gray')
    axes[0].set_title("Original Image")
    axes[0].axis('off')

    axes[1].imshow(R, cmap='hot')
    axes[1].set_title("Harris Response (R)")
    axes[1].axis('off')

    axes[2].imshow(corner_image, cmap='gray')
    axes[2].set_title("Thresholded Corners (Scratch)")
    axes[2].axis('off')

    axes[3].imshow(img_color)
    axes[3].set_title("Corners Overlay (Scratch)")
    axes[3].axis('off')

    plt.tight_layout()
    os.makedirs('outputs', exist_ok=True)
    plt.savefig('outputs/08_harris.png', dpi=100)
    plt.close(fig)

if __name__ == "__main__":
    np.random.seed(42)
    main()
