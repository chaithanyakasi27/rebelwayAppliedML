import cv2
import easyocr
import numpy as np

# Path to the input image
image_path = "image.jpg"

# Load the image
img = cv2.imread(image_path)

# Preprocess: Convert to grayscale and apply adaptive thresholding
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 11, 2)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Run OCR
result = reader.readtext(img)

# Confidence threshold
threshold = 0.3

# Draw bounding boxes and labels
for i, t in enumerate(result):
    bbox, text, score = t

    if score > threshold:
        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))

        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(img, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 12), 2)

# Save output image
cv2.imwrite("output.jpg", img)
print("Saved output to output.jpg")
