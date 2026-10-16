"""
Module: Hough Transform

The Hough transform is a technique for finding perfect shapes like lines and circles. It works by casting votes in a parameter space. The peaks in this parameter space correspond to the shapes found in the image.
"""

import os
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_lines_image():
    """Creates a synthetic image with lines."""
    img = np.zeros((300, 300), dtype=np.uint8)

    # Draw some lines
    cv2.line(img, (50, 50), (250, 250), 255, 3)
    cv2.line(img, (250, 50), (50, 250), 255, 3)
    cv2.line(img, (10, 150), (290, 150), 255, 3)

    # Add some noise
    noise = np.random.randint(0, 50, img.shape, dtype=np.uint8)
    img = cv2.add(img, noise)

    return img

def create_circles_image():
    """Creates a synthetic image with circles."""
    img = np.zeros((300, 300), dtype=np.uint8)

    # Draw some circles (filled and outlined)
    cv2.circle(img, (150, 150), 60, 255, -1) # Solid
    cv2.circle(img, (80, 80), 30, 255, 3)    # Outline
    cv2.circle(img, (220, 220), 40, 255, 5)  # Thick outline

    # Add noise
    noise = np.random.randint(0, 50, img.shape, dtype=np.uint8)
    img = cv2.add(img, noise)

    return img

def detect_lines():
    img = create_lines_image()

    # 1. Edge detection is required first
    edges = cv2.Canny(img, 50, 150, apertureSize=3)

    # 2. Apply Hough Line Transform (Standard)
    # rho = 1 pixel, theta = 1 degree (np.pi/180), threshold = 100 votes
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

    output_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            # Convert polar coordinates to Cartesian for drawing
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            # Calculate two points along the line
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(output_img, (x1, y1), (x2, y2), (255, 0, 0), 2)

    return img, edges, output_img

def detect_circles():
    img = create_circles_image()

    # Needs a slight blur to reduce false circles from noise
    blurred = cv2.medianBlur(img, 5)

    # Apply Hough Circle Transform
    # param1 is Canny threshold, param2 is accumulator threshold
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=20, maxRadius=100)

    output_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Draw the outer circle
            cv2.circle(output_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Draw the center of the circle
            cv2.circle(output_img, (i[0], i[1]), 2, (0, 0, 255), 3)

    return img, output_img

def main():
    # 1. Lines
    lines_orig, lines_edges, lines_out = detect_lines()

    fig1, axes1 = plt.subplots(1, 3, figsize=(15, 5))
    axes1[0].imshow(lines_orig, cmap='gray')
    axes1[0].set_title("Original Lines Image")
    axes1[0].axis('off')

    axes1[1].imshow(lines_edges, cmap='gray')
    axes1[1].set_title("Canny Edges")
    axes1[1].axis('off')

    axes1[2].imshow(lines_out)
    axes1[2].set_title("Detected Lines")
    axes1[2].axis('off')

    os.makedirs('outputs', exist_ok=True)
    fig1.savefig('outputs/10_hough_lines.png', dpi=100)
    plt.close(fig1)

    # 2. Circles
    circles_orig, circles_out = detect_circles()

    fig2, axes2 = plt.subplots(1, 2, figsize=(10, 5))
    axes2[0].imshow(circles_orig, cmap='gray')
    axes2[0].set_title("Original Circles Image")
    axes2[0].axis('off')

    axes2[1].imshow(circles_out)
    axes2[1].set_title("Detected Circles")
    axes2[1].axis('off')

    fig2.savefig('outputs/10_hough_circles.png', dpi=100)
    plt.close(fig2)

if __name__ == "__main__":
    np.random.seed(42)
    main()
