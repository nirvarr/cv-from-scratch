"""
Module: HOG Features and SVM

Histogram of Oriented Gradients (HOG) is a powerful feature descriptor for shape representation. We will extract HOG features from a synthetic dataset of shapes. Finally, we'll train a Support Vector Machine (SVM) to classify them and evaluate its accuracy.
"""

import os
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from skimage.feature import hog

def create_synthetic_dataset(num_samples=200):
    """
    Creates a synthetic dataset of circles (label 0) and squares (label 1).
    Returns images and labels.
    """
    images = []
    labels = []

    img_size = 64

    for _ in range(num_samples // 2):
        # Create circle
        img = np.zeros((img_size, img_size), dtype=np.uint8)
        center = (np.random.randint(20, 44), np.random.randint(20, 44))
        radius = np.random.randint(10, 20)
        cv2.circle(img, center, radius, 255, -1)

        # Add noise
        noise = np.random.randint(0, 50, img.shape, dtype=np.uint8)
        img = cv2.add(img, noise)

        images.append(img)
        labels.append(0)

    for _ in range(num_samples // 2):
        # Create square
        img = np.zeros((img_size, img_size), dtype=np.uint8)
        top_left = (np.random.randint(10, 34), np.random.randint(10, 34))
        side = np.random.randint(20, 40)
        bottom_right = (top_left[0] + side, top_left[1] + side)
        cv2.rectangle(img, top_left, bottom_right, 255, -1)

        # Add noise
        noise = np.random.randint(0, 50, img.shape, dtype=np.uint8)
        img = cv2.add(img, noise)

        images.append(img)
        labels.append(1)

    # Shuffle dataset
    dataset = list(zip(images, labels))
    np.random.shuffle(dataset)

    images, labels = zip(*dataset)
    return np.array(images), np.array(labels)

def extract_features(images):
    """Extracts HOG features for all images."""
    features = []
    for img in images:
        fd = hog(img, orientations=8, pixels_per_cell=(16, 16),
                 cells_per_block=(1, 1), visualize=False)
        features.append(fd)
    return np.array(features, dtype=np.float32)

def main():
    # 1. Setup Data
    print("Generating dataset...")
    X_imgs, y = create_synthetic_dataset(400)

    # Split into train and test
    split_idx = int(0.8 * len(X_imgs))
    X_train_imgs, X_test_imgs = X_imgs[:split_idx], X_imgs[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # 2. Extract Features
    print("Extracting HOG features...")
    X_train = extract_features(X_train_imgs)
    X_test = extract_features(X_test_imgs)

    # 3. Train SVM Model (OpenCV)
    print("Training SVM...")
    svm = cv2.ml.SVM_create()
    svm.setType(cv2.ml.SVM_C_SVC)
    svm.setKernel(cv2.ml.SVM_LINEAR)
    svm.setTermCriteria((cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-6))

    # Convert labels to int32 as required by OpenCV
    svm.train(X_train, cv2.ml.ROW_SAMPLE, np.array(y_train, dtype=np.int32))

    # 4. Evaluate
    _, y_pred = svm.predict(X_test)
    y_pred = y_pred.flatten().astype(int)

    accuracy = np.mean(y_pred == y_test)
    print(f"Accuracy: {accuracy * 100:.2f}%")

    # Compute confusion matrix
    cm = np.zeros((2, 2), dtype=int)
    for true_label, pred_label in zip(y_test, y_pred):
        cm[true_label, pred_label] += 1

    # 5. Visualization
    fig, ax = plt.subplots(figsize=(6, 5))

    cax = ax.matshow(cm, cmap='Blues')
    fig.colorbar(cax)

    # Add text annotations
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), va='center', ha='center',
                    color='white' if cm[i, j] > cm.max() / 2. else 'black')

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['Circle (0)', 'Square (1)'])
    ax.set_yticklabels(['Circle (0)', 'Square (1)'])
    ax.set_xlabel('Predicted Label')
    ax.set_ylabel('True Label')
    ax.set_title(f'Confusion Matrix\nAccuracy: {accuracy * 100:.1f}%')

    plt.tight_layout()
    os.makedirs('outputs', exist_ok=True)
    plt.savefig('outputs/12_confusion_matrix.png', dpi=100)
    plt.close(fig)

if __name__ == "__main__":
    np.random.seed(42)
    main()
