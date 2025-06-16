import cv2
import numpy as np
import mediapipe as mp
import os

# Initialize MediaPipe components
mp_draw = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Input video path
source = r"/home/kasir20/development/rebelwayAppliedML/computer_vision/mediapipe/Jump.mp4"
output_path = r"/home/kasir20/development/rebelwayAppliedML/computer_vision/mediapipe/Jump_output.mp4"

# Open video
cap = cv2.VideoCapture(source)

# Get frame size and FPS from the input video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Define codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or use 'XVID' for AVI
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Set up MediaPipe Pose
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, image = cap.read()

        if not ret:
            break

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            mp_draw.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style()
            )

        # Display and write output frame
        cv2.imshow("Pose Detection", image)
        out.write(image)  # Save frame to output video

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
