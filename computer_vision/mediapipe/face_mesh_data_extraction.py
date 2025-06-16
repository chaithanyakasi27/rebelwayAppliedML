import cv2
import numpy as np
import mediapipe as mp
import os
import json

# Input and output paths
source = '/home/kasir20/development/rebelwayAppliedML/computer_vision/mediapipe/facemesh_2.mp4'
output_path = '/home/kasir20/development/rebelwayAppliedML/computer_vision/mediapipe/output_facemesh.mp4'

# Open input video
cap = cv2.VideoCapture(source)
if not cap.isOpened():
    print("Error: Unable to open input video.")
    exit()

# Mediapipe face mesh setup
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec1 = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2)
drawSpec2 = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=2)

landmarks_data = []

# Process frames
while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        print("Reached end of video or failed to read frame.")
        break

    # Resize frame
    scale_val = 0.8
    x1 = int(img.shape[1] * scale_val)
    x2 = int(img.shape[0] * scale_val)
    img = cv2.resize(img, (x1, x2))

    # Convert to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detections = faceMesh.process(imgRGB)

    # Draw mesh
    if detections.multi_face_landmarks:
        face_landmark = detections.multi_face_landmarks[0]
        frame_landmarks = []

        for landmark in face_landmark.landmark:
            frame_landmarks.append({
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z
            })
        landmarks_data.append(frame_landmarks)

        mpDraw.draw_landmarks(img, face_landmark, mpFaceMesh.FACEMESH_CONTOURS, drawSpec1, drawSpec2)

    # Show frame
    cv2.imshow("Face Mesh", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()

print(f"Video saved to: {output_path}")

output_file = "face_landmarks.json"

with open(output_file, "w") as f:
    json.dump(landmarks_data, f, indent =4)

print("Landmarks saved")
