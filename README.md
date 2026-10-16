# cv-from-scratch

A project that teaches computer vision fundamentals from the ground up through runnable examples, plus a daily-delivery system (push notification + installable offline web app).

## Learning Path

1. **Images as Arrays**: Understand images as numpy arrays, pixels, channels, and RGB vs grayscale.
2. **Color Spaces**: Learn about HSV, LAB, and color-based segmentation.
3. **Histograms**: Explore histograms and contrast stretching/equalization.
4. **Convolution**: Implement convolution from scratch and compare blur and sharpen kernels against OpenCV.
5. **Edge Detection**: Build Sobel from scratch and explore the Canny edge detector.
6. **Thresholding and Morphology**: Apply global, Otsu, and adaptive thresholding along with morphological operations (erode, dilate, open, close).
7. **Contours and Shape Measurements**: Detect contours, find connected components, and measure simple shapes.
8. **Harris Corner Detection**: Implement Harris corner detection from scratch.
9. **Template Matching**: Learn how to match templates in an image.
10. **Hough Transform**: Detect lines and circles using the Hough transform.
11. **Feature Detection and Matching**: Detect and match features with ORB.
12. **Capstone (HOG + SVM)**: Extract HOG features from synthetic data and classify with an SVM.

## Setup

1. Create a GitHub repo and push this codebase.
2. Set the `NTFY_TOPIC` repository secret (Settings > Secrets and variables > Actions) to a long, hard-to-guess topic name.
3. Enable GitHub Pages (Settings > Pages > Deploy from a branch > main > /docs).
4. Install the ntfy app on Android and subscribe to the `NTFY_TOPIC`. Alternatively, subscribe on your MacBook (ntfy app or ntfy.sh browser).
5. Install the PWA from your GitHub Pages URL (e.g., `https://<owner>.github.io/cv-from-scratch/`) on Android and macOS.
6. Manually trigger the daily-lesson workflow once from the Actions tab to test.

## Adding a new lesson

1. Run `python tools/new_lesson.py <number> <name>` (e.g., `python tools/new_lesson.py 13 test`).
2. Write the lesson in `lessons/13_test.py`.
3. Add the title, 3-sentence summary, and figure names to `lessons.json`.
4. Run `python run_all.py` to ensure it works.
5. Run `python tools/build_docs.py` to update the web app.
6. Run `pytest` to check tests.
7. Commit and push the changes.
