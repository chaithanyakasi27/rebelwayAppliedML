import cv2
import easyocr
import numpy as np
import torch

# Check if GPU is available and print the device being used
use_gpu = torch.cuda.is_available()
print(f"Using GPU: {use_gpu}")
print(f"Device: {torch.cuda.get_device_name(0) if use_gpu else 'CPU'}")

# Initialize EasyOCR reader with English language and GPU support if available
reader = easyocr.Reader(['en'], gpu=use_gpu)

# Load input video file
input_path = '/content/book.mp4'
cap = cv2.VideoCapture(input_path)

# Verify video file opened successfully
if not cap.isOpened():
    print(f"Error: Cannot open video file {input_path}")
    exit()

# Retrieve video properties: frames per second, frame width and height
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Video properties - FPS: {fps}, Width: {width}, Height: {height}")

# Setup video writer to save processed video output with the same properties as input
output_path = 'output_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4 output
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Check if VideoWriter opened correctly
if not out.isOpened():
    print("Error: VideoWriter not opened")
    cap.release()
    exit()

# Process video frame by frame
while True:
    ret, frame = cap.read()  # Read a single frame
    if not ret:
        break  # Exit loop if no more frames

    # Perform OCR detection and recognition on the frame
    # paragraph=True attempts to group words into paragraphs
    # detail=1 returns bounding boxes and recognized text
    results = reader.readtext(frame, paragraph=True, detail=1)

    # Loop through detected text blocks
    for bbox, text in results:
        # Convert bounding box points to integer numpy array
        pts = np.array(bbox).astype(int)

        # Calculate bounding rectangle coordinates
        x_min = np.min(pts[:, 0])
        y_min = np.min(pts[:, 1])
        x_max = np.max(pts[:, 0])
        y_max = np.max(pts[:, 1])

        # Draw green rectangle around detected text block
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        # Position for text overlay: above the rectangle if space allows, else below
        text_pos = (x_min, y_min - 10 if y_min - 10 > 10 else y_min + 20)

        # Put detected text on frame in green color
        cv2.putText(frame, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Write processed frame with overlays to output video file
    out.write(frame)

# Release video capture and writer resources
cap.release()
out.release()

print("Saved output to:", output_path)
