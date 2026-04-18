from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Tuple, List, Dict


class ParkingDetector:
    def __init__(self, model_path: str = "best.pt", conf: float = 0.4):
        self.model = YOLO(model_path)
        self.conf = conf
        self.target_size = (960, 600)

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, List[Dict]]:
        """Обрабатывает один кадр и возвращает размеченный кадр + список свободных мест"""
        if frame is None:
            return None, []

        frame = cv2.resize(frame, self.target_size)

        results = self.model(frame, conf=self.conf, verbose=False)
        boxes = results[0].boxes

        output = frame.copy()
        free_spots = []

        for box in boxes:
            cls_id = int(box.cls[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Фильтры мусора
            if x2 - x1 < 20 or y2 - y1 < 20:
                continue

            if cls_id == 0:  # FREE
                color = (0, 255, 0)
                label = "FREE"
                free_spots.append({
                    "bbox": [x1, y1, x2, y2],
                    "center": [(x1 + x2) // 2, (y1 + y2) // 2]
                })
            else:
                color = (0, 0, 255)
                label = "BUSY"

            cv2.rectangle(output, (x1, y1), (x2, y2), color, 2)
            text_y = y1 - 8 if y1 > 25 else y1 + 20
            cv2.putText(output, label, (x1, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Информация сверху
        cv2.putText(output, f"FREE: {len(free_spots)}", (15, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(output, f"TOTAL: {len(boxes)}", (15, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        return output, free_spots

    # ======================= Новые методы =======================

    def detect_image(self, image_bytes: bytes) -> Tuple[bytes, List[Dict], int]:
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            raise ValueError("Не удалось прочитать изображение")

        processed, free_spots = self.process_frame(frame)

        success, encoded = cv2.imencode('.jpg', processed, [cv2.IMWRITE_JPEG_QUALITY, 90])
        return encoded.tobytes(), free_spots, len(free_spots)

    def run_camera(self, camera_id: int = 0):
        """Запуск с веб-камеры"""
        cap = cv2.VideoCapture(camera_id)
        self._run_video_loop(cap, source_type="camera")

    def run_video_file(self, video_path: str):
        """Запуск с видеофайла"""
        cap = cv2.VideoCapture(video_path)
        self._run_video_loop(cap, source_type="video")

    def _run_video_loop(self, cap: cv2.VideoCapture, source_type: str):
        if not cap.isOpened():
            print("❌ Не удалось открыть источник")
            return

        print(f"✅ Запущен {source_type}... (Нажми Q для выхода)")

        while True:
            ret, frame = cap.read()
            if not ret:
                if source_type == "video":
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # зациклить видео
                    continue
                else:
                    break

            processed, free_spots = self.process_frame(frame)

            cv2.imshow(f"Smart Parking AI - {source_type}", processed)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            if key == ord('n') and free_spots:
                # Открываем навигацию к первому свободному месту
                cx, cy = free_spots[0]["center"]
                lat = 42.8746 + (cy / 10000)
                lon = 74.5698 + (cx / 10000)
                import webbrowser
                webbrowser.open(f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}")

        cap.release()
        cv2.destroyAllWindows()