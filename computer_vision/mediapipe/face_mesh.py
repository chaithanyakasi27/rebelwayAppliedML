import cv2
import numpy as np
import mediapipe as mp
import os

# Input and output paths
source = '/home/kasir20/development/rebelwayAppliedML/computer_vision/mediapipe/facemesh_2.mp4'
output_path = '/home/kasir20/development/rebelwayAppliedML/computer_vision/mediapipe/output_facemesh.mp4'

# Open input video
cap = cv2.VideoCapture(source)
if not cap.isOpened():
    print("Error: Unable to open input video.")
    exit()

# Get original video properties
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * 0.8)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * 0.8)

# Define VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Mediapipe face mesh setup
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec1 = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2)
drawSpec2 = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=2)

# Process frames
while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        print("Reached end of video or failed to read frame.")
        break

    # Resize frame
    img = cv2.resize(img, (width, height))

    # Convert to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detections = faceMesh.process(imgRGB)

    # Draw mesh
    if detections.multi_face_landmarks:
        for face_landmark in detections.multi_face_landmarks:
            mpDraw.draw_landmarks(img, face_landmark, mpFaceMesh.FACEMESH_CONTOURS, drawSpec1, drawSpec2)

    # Show frame
    cv2.imshow("Face Mesh", img)

    # Write to output file
    out.write(img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Video saved to: {output_path}")
