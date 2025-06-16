import cv2
import mediapipe as mp
import numpy as np

class FaceDetector:
    def __init__(self, minimumDetectionConfidence=0.5):
        # Store minimum confidence threshold for detection
        self.minDectCon = minimumDetectionConfidence
        self.draw_mp = mp.solutions.drawing_utils
        # Initialize MediaPipe Face Detection
        self.faceDetection = mp.solutions.face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=self.minDectCon
        )

    def findFaces(self, img, draw=True):
        # Convert BGR image to RGB for MediaPipe
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Process image to find faces
        self.detection_results = self.faceDetection.process(image)

        detections = []

        if self.detection_results.detections:
            for id, detection in enumerate(self.detection_results.detections):
                # Extract bounding box coordinates relative to the image
                bbox_data = detection.location_data.relative_bounding_box
                h, w, c = img.shape
                bbox = (
                    int(bbox_data.xmin * w),
                    int(bbox_data.ymin * h),
                    int(bbox_data.width * w),
                    int(bbox_data.height * h)
                )

                detections.append([id, bbox, detection.score])

                if draw:
                    # Draw bounding box and confidence score
                    img = self.drawShapes(img, bbox)
                    cv2.putText(
                        img,
                        f'{int(detection.score[0] * 100)}%',
                        (bbox[0], bbox[1] - 10),
                        cv2.FONT_HERSHEY_PLAIN,
                        2,
                        (0, 255, 0),
                        2
                    )

        return img, detections

    def drawShapes(self, img, bbox):
        # Draw rectangle around detected face
        x, y, w, h = bbox
        cv2.rectangle(img, bbox, (0, 255, 0), 2)
        return img

def main():
    # Input and output video paths
    video_path = r"D:\portfolio class\3D\development\ML\rebelwayAppliedML\computer_vision\mediapipe\people_faces.mp4"
    output_path = r"D:\portfolio class\3D\development\ML\rebelwayAppliedML\computer_vision\mediapipe\output_faces.mp4"

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Error: Cannot open video file {video_path}")
        return

    detector = FaceDetector()

    # Target resolution (to reduce output video size)
    target_width = 640
    target_height = 360
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Set up video writer for saving output
    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (target_width, target_height)
    )

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        # Resize image before detection to avoid zoom issues
        img = cv2.resize(img, (target_width, target_height))

        # Detect faces and draw bounding boxes
        img, bbox = detector.findFaces(img)

        # Write the frame to the output video
        out.write(img)

        # Optional: Display the frame
        cv2.imshow("Faces", img)
        if cv2.waitKey(1) == ord('q'):
            break

    # Clean up
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"✅ Output video saved to: {output_path}")

if __name__ == "__main__":
    main()
