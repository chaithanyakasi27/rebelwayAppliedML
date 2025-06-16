import cv2
import mediapipe as mp

source = r'D:\portfolio class\3D\development\ML\rebelwayAppliedML\computer_vision\mediapipe\facemesh.mp4'
cap = cv2.VideoCapture(source)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2)

# Get original video dimensions
orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_facemesh.mp4', fourcc, fps, (orig_width, orig_height))

while True:
    ret, img = cap.read()
    if not ret:
        print("End of video reached or can't fetch the frame.")
        break

    # Optional: resize frame (keep original size for output)
    scale_val = 0.8
    new_width = int(orig_width * scale_val)
    new_height = int(orig_height * scale_val)
    img_small = cv2.resize(img, (new_width, new_height))

    imgRGB = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Draw on the smaller image (to reduce load)
            mpDraw.draw_landmarks(img_small, face_landmarks, mpFaceMesh.FACEMESH_CONTOURS, drawSpec)

    # Resize back to original size for output and display
    output_frame = cv2.resize(img_small, (orig_width, orig_height))

    out.write(output_frame)  # Write frame to video file

    cv2.imshow("Face Mesh", output_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Quit pressed, stopping...")
        break

cap.release()
out.release()
cv2.destroyAllWindows()

