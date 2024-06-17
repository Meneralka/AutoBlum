import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import threading


def capture_screen():
    screen = np.array(ImageGrab.grab())
    return screen


def create_mask(screen_bgr):
    # Создаём маску для опознания звёздочек
    lower = np.array((41, 255, 129), dtype="uint8")
    upper = np.array((186, 255, 226), dtype="uint8")
    mask = cv2.inRange(screen_bgr, lower, upper)

    return mask


def find_targets(screen):
    # Конвертируем изображение в формат BGR для использования в OpenCV
    screen_bgr = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    mask = create_mask(screen_bgr)

    # Находим контуры объектов на маске
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Находим центры контуров
    centers = []
    for contour in contours:
        if cv2.contourArea(contour) > 5:  # Игнорируем слишком маленькие контуры
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M['m00'])
                cY = int(M["m01"] / M['m00'])
                centers.append((cX, cY))

    return centers


def bbb(x, y):
    pyautogui.click(x, y)
    print(f'Нажал на звёздочку {x} {y}')


def main():
    print("Скрипт начал работу!")
    while True:
        screen = capture_screen()
        targets = find_targets(screen)
        for (x, y) in targets:
            threading.Thread(target=bbb, args=(x, y), daemon=True).start()


if __name__ == "__main__":
    main()
