"""
Module: Histograms

A histogram shows the distribution of pixel intensities in an image. Contrast stretching spreads out these intensities to improve visibility. Histogram equalization flattens the distribution for even more contrast enhancement.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from skimage import data

def get_low_contrast_image():
    """Gets a low contrast image."""
    # The 'moon' image is grayscale and somewhat low contrast
    img = data.moon()
    # Artificially lower contrast for better demonstration
    img = (img * 0.5 + 50).astype(np.uint8)
    return img

def compute_histogram(image):
    """Computes a histogram from scratch."""
    hist = np.zeros(256, dtype=int)
    # Using np.bincount is a fast way to do this from scratch in numpy
    # Equivalent to a for loop over all pixels: hist[pixel_value] += 1
    counts = np.bincount(image.ravel(), minlength=256)
    hist[:len(counts)] = counts
    return hist

def histogram_equalization(image):
    """Performs histogram equalization from scratch."""
    hist = compute_histogram(image)

    # Compute Cumulative Distribution Function (CDF)
    cdf = hist.cumsum()

    # Normalize CDF to range [0, 255]
    # We ignore zeros in CDF to avoid division by zero issues in stretching
    cdf_masked = np.ma.masked_equal(cdf, 0)
    cdf_normalized = (cdf_masked - cdf_masked.min()) * 255 / (cdf_masked.max() - cdf_masked.min())
    cdf_normalized = np.ma.filled(cdf_normalized, 0).astype(np.uint8)

    # Apply mapping to original image
    img_equalized = cdf_normalized[image]
    return img_equalized

def main():
    # 1. Setup
    img = get_low_contrast_image()

    # 2. Process data
    img_eq = histogram_equalization(img)

    hist_orig = compute_histogram(img)
    hist_eq = compute_histogram(img_eq)

    # 3. Visualization
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # Original Image and Histogram
    axes[0, 0].imshow(img, cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title("Low Contrast Original")
    axes[0, 0].axis('off')

    axes[0, 1].plot(hist_orig, color='black')
    axes[0, 1].set_title("Original Histogram")
    axes[0, 1].set_xlim([0, 256])
    axes[0, 1].fill_between(range(256), hist_orig, color='gray', alpha=0.5)

    # Equalized Image and Histogram
    axes[1, 0].imshow(img_eq, cmap='gray', vmin=0, vmax=255)
    axes[1, 0].set_title("Histogram Equalized")
    axes[1, 0].axis('off')

    axes[1, 1].plot(hist_eq, color='black')
    axes[1, 1].set_title("Equalized Histogram")
    axes[1, 1].set_xlim([0, 256])
    axes[1, 1].fill_between(range(256), hist_eq, color='gray', alpha=0.5)

    plt.tight_layout()
    os.makedirs('outputs', exist_ok=True)
    plt.savefig('outputs/03_histograms.png', dpi=100)
    plt.close(fig)

if __name__ == "__main__":
    np.random.seed(42)
    main()
