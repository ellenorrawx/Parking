import sys
from pathlib import Path
import cv2

# Добавляем корневую папку в путь
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from parking_app.ai.parking_detector import ParkingDetector

# ================== НАСТРОЙКИ ==================
MODEL_PATH = str(ROOT_DIR / "best.pt")

# Выбери режим работы (раскомментируй только один):
MODE = "video"  # варианты: "image", "camera", "video"

# Для видео режима — укажи путь к видеофайлу
VIDEO_PATH = str(ROOT_DIR / "parking_crop.mp4")  # ← сюда положишь видео с Kaggle

print(f"🚀 Запуск Smart Parking AI")
print(f"Модель: {MODEL_PATH}")

detector = ParkingDetector(model_path=MODEL_PATH, conf=0.4)
print("✅ Модель успешно загружена!\n")

# ====================== РЕЖИМЫ ======================

if MODE == "image":
    print("🖼️  Режим: Статичное изображение")
    image_path = str(ROOT_DIR / "0.png")
    frame = cv2.imread(image_path)

    if frame is None:
        print(f"❌ Не удалось открыть изображение: {image_path}")
        exit()

    while True:
        processed, free_spots = detector.process_frame(frame)
        cv2.imshow("Smart Parking AI - Изображение", processed)

        print(f"Свободных мест: {len(free_spots)}     ", end="\r")

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

elif MODE == "camera":
    print("📹 Режим: Веб-камера (реальное время)")
    detector.run_camera(camera_id=0)  # 0 = встроенная камера ноутбука

elif MODE == "video":
    print("🎥 Режим: Видеофайл (реальное время)")
    print(f"Видео: {VIDEO_PATH}")

    if not Path(VIDEO_PATH).exists():
        print(f"❌ Видео не найдено: {VIDEO_PATH}")
        print("Скачай видео с Kaggle и положи его в корень проекта как parking_loop.mp4")
        input("Нажми Enter когда скачаешь...")
    else:
        detector.run_video_file(VIDEO_PATH)

else:
    print("❌ Неправильный MODE в run_ai_main.py")

cv2.destroyAllWindows()
print("\nПрограмма завершена.")