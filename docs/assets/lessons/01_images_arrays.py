"""
Module: Images as Arrays

Images are just grids of numbers representing pixel intensities. We will learn how to inspect these numbers as numpy arrays. We'll also see the difference between RGB and grayscale images.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_synthetic_image():
    """Generates a simple 3-channel (RGB) synthetic image."""
    # Create a 100x100 RGB image with a gradient background
    img = np.zeros((100, 100, 3), dtype=np.uint8)

    # Red gradient horizontally
    for i in range(100):
        img[:, i, 0] = int((i / 99) * 255)

    # Green gradient vertically
    for j in range(100):
        img[j, :, 1] = int((j / 99) * 255)

    # Blue constant patch in the middle
    img[30:70, 30:70, 2] = 255

    return img

def rgb_to_grayscale(rgb_img):
    """
    Converts an RGB image to grayscale from scratch.
    Using the standard luminosity formula: Y = 0.299*R + 0.587*G + 0.114*B
    """
    # Separate channels (assuming RGB order)
    r = rgb_img[:, :, 0]
    g = rgb_img[:, :, 1]
    b = rgb_img[:, :, 2]

    # Apply weights and convert back to uint8
    gray = 0.299 * r + 0.587 * g + 0.114 * b
    return gray.astype(np.uint8)

def main():
    # 1. Setup and data generation
    img_rgb = create_synthetic_image()

    # 2. Process data
    img_gray = rgb_to_grayscale(img_rgb)

    # Let's inspect the shapes
    print(f"RGB image shape: {img_rgb.shape} - (Height, Width, Channels)")
    print(f"Grayscale image shape: {img_gray.shape} - (Height, Width)")

    # 3. Visualization
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))

    # Display RGB image
    axes[0].imshow(img_rgb)
    axes[0].set_title(f"RGB Image\nShape: {img_rgb.shape}")
    axes[0].axis('off')

    # Display Grayscale image using gray colormap
    axes[1].imshow(img_gray, cmap='gray')
    axes[1].set_title(f"Grayscale Image\nShape: {img_gray.shape}")
    axes[1].axis('off')

    plt.tight_layout()

    # Save output with deterministic name and small size
    os.makedirs('outputs', exist_ok=True)
    plt.savefig('outputs/01_rgb_vs_gray.png', dpi=100)
    plt.close(fig)

if __name__ == "__main__":
    np.random.seed(42)
    main()
