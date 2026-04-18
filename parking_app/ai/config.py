from pathlib import Path

# ========================= НАСТРОЙКИ МОДЕЛИ =========================

# Путь к модели (можно изменить)
MODEL_PATH = "best.pt"                    # лежит в корне Parking/

# Параметры обработки
CONFIDENCE_THRESHOLD = 0.4
TARGET_WIDTH = 960
TARGET_HEIGHT = 600

# Координаты для демо-навигации (Бишкек)
DEFAULT_LAT = 42.8746
DEFAULT_LON = 74.5698

# Расширения файлов
VIDEO_EXT = ('.mp4', '.avi', '.mov', '.mkv', '.wmv')
IMAGE_EXT = ('.png', '.jpg', '.jpeg', '.bmp', '.webp')