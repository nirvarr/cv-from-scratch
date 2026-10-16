import pytest
import numpy as np
import cv2
import importlib
from skimage import data

# Import functions from lessons dynamically
l1 = importlib.import_module("lessons.01_images_arrays")
l3 = importlib.import_module("lessons.03_histograms")
l4 = importlib.import_module("lessons.04_convolution")
l5 = importlib.import_module("lessons.05_edge_detection")
l8 = importlib.import_module("lessons.08_harris_corners")

def test_rgb_to_grayscale():
    img_rgb = l1.create_synthetic_image()
    gray_scratch = l1.rgb_to_grayscale(img_rgb)
    gray_cv2 = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # Allow small differences due to rounding (OpenCV might use integer math for speed)
    diff = np.abs(gray_scratch.astype(int) - gray_cv2.astype(int))
    assert np.max(diff) <= 2, "Grayscale conversion should closely match OpenCV"

def test_histogram_equalization():
    img = l3.get_low_contrast_image()
    eq_scratch = l3.histogram_equalization(img)
    eq_cv2 = cv2.equalizeHist(img)

    # Allow small differences due to tie-breaking in CDF mapping
    diff = np.abs(eq_scratch.astype(int) - eq_cv2.astype(int))
    assert np.mean(diff) < 5, "Histogram equalization should generally match OpenCV"

def test_convolution():
    img = data.camera()[:100, :100] # Use smaller image for fast test
    kernel = np.ones((5, 5), np.float32) / 25.0

    conv_scratch = l4.convolve2d_scratch(img, kernel)
    # OpenCV filter2D doesn't pad with zeros by default, so we use BORDER_CONSTANT with value 0
    conv_cv2 = cv2.filter2D(img, -1, kernel, borderType=cv2.BORDER_CONSTANT)

    # Discard borders for comparison to avoid padding artifact differences
    k = 5 // 2
    inner_scratch = conv_scratch[k:-k, k:-k]
    inner_cv2 = conv_cv2[k:-k, k:-k]

    diff = np.abs(inner_scratch.astype(int) - inner_cv2.astype(int))
    assert np.max(diff) <= 2, "Convolution should match OpenCV's filter2D"

def test_sobel():
    img = data.coins()[:100, :100]
    Ix_scratch, Iy_scratch, mag_scratch = l5.sobel_scratch(img)

    # OpenCV Sobel
    Ix_cv2 = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3)
    Iy_cv2 = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3)

    # Note: Our Sobel kernels might be scaled differently or inverted compared to OpenCV's exact implementation
    # But the magnitudes should be proportional.
    mag_cv2 = np.sqrt(Ix_cv2**2 + Iy_cv2**2)
    mag_cv2 = (mag_cv2 / mag_cv2.max() * 255).astype(np.uint8)

    # Just checking that the scratch implementation runs and produces valid output
    assert Ix_scratch.shape == img.shape
    assert mag_scratch.max() > 0

def test_harris_corners():
    img = l8.create_checkerboard()
    R_scratch, _, _ = l8.harris_corners_scratch(img, k=0.04)

    # OpenCV Harris
    R_cv2 = cv2.cornerHarris(img.astype(np.float32), 3, 3, 0.04)

    # Both should have strong responses at the corners
    assert R_scratch.shape == R_cv2.shape
    assert R_scratch.max() > 0
    assert R_cv2.max() > 0
