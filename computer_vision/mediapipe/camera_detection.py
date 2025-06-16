import cv2
import mediapipe as mp
import numpy as np

class FaceDetector:
    def __init__(self, minimumDetectionConfidence=0.5):
        # Confidence threshold for face detection
        self.minDectCon = minimumDetectionConfidence
        self.draw_mp = mp.solutions.drawing_utils
        # Initialize MediaPipe face detector
        self.faceDetection = mp.solutions.face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=self.minDectCon
        )

    def findFaces(self, img, draw=True):
        # Convert BGR to RGB
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.detection_results = self.faceDetection.process(image)

        detections = []
        img.flags.writeable = True

        if self.detection_results.detections:
            for id, detection in enumerate(self.detection_results.detections):
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
        # Draw bounding box
        x, y, w, h = bbox
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return img


def main():
    print("[INFO] Starting camera...")
    video_path = 0  # Webcam
    output_path = 'output_faces.mp4'

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(" Error: Cannot access camera.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps != fps:  # NaN check
        fps = 30.0

    target_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    target_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"[INFO] Webcam resolution: {target_width}x{target_height} @ {fps} FPS")

    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (target_width, target_height)
    )

    detector = FaceDetector()

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            print("[WARN] Could not read frame from camera.")
            break

        img, bbox = detector.findFaces(img)
        out.write(img)

        cv2.imshow("Face Detection - Press 'q' to quit", cv2.flip(img, 1))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"[INFO] Output video saved to: {output_path}")


if __name__ == "__main__":
    main()
