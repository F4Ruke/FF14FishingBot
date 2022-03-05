from numpy import array, where
from cv2 import cv2
from time import sleep
from win32api import GetSystemMetrics
from keyboard import wait, add_hotkey, send
from pyautogui import screenshot
from random import uniform


def change_image(image):
    """Перевод картинки в бинарный режим"""
    image = array(image)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(image_gray, 230, 230, cv2.THRESH_BINARY)
    return binary


def search_image(image, template):
    """Поиск шаблона (template) на изображении (image)"""
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    return where(res >= 0.7)


def cut_image(image):
    """Обрезка изображения"""
    return image[GetSystemMetrics(1) // 2 - 200:GetSystemMetrics(1) // 2 + 200,
                 GetSystemMetrics(0) // 2 - 100:GetSystemMetrics(0) // 2 + 100]


def main():
    flag = True
    TEMPLATE = (change_image(cv2.imread("ScreenShots/1.png")),
                change_image(cv2.imread("ScreenShots/2.png")))

    while True:
        if flag:
            send("1")  # Забрасываем удочку
            flag = False

        img_gray = cut_image(change_image(screenshot()))
        loc_matrix = (search_image(img_gray, TEMPLATE[0]),
                      search_image(img_gray, TEMPLATE[1]))

        for i in range(len(loc_matrix)):
            if len(loc_matrix[i][0]) and not flag:
                send("2")  # Достаем рыбку
                flag = True
                sleep(uniform(11, 13))


if __name__ == "__main__":
    add_hotkey("f10", main)
    wait()
