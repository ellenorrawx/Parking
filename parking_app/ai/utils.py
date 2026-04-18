import cv2

def draw_text(img, text, pos, scale=0.6, color=(255, 255, 255), thickness=2):
    """Удобная функция для рисования текста с тенью"""
    x, y = pos
    # Тень
    cv2.putText(img, text, (x+2, y+2),
                cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 0), thickness+1)
    # Основной текст
    cv2.putText(img, text, (x, y),
                cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)


def clamp(value, min_val, max_val):
    """Ограничивает значение в диапазоне"""
    return max(min_val, min(value, max_val))