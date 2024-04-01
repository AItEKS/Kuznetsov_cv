import pyautogui as gui
import keyboard
import cv2
import numpy as np
import time
import math


def get_pixel(image, x, y):
    if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
        return image[y, x]
    else:
        return None


def start():
    x, y, width, height = 710, 180, 1260, 350
    jumping_time = 0
    last_jumping_time = 0
    last_interval_time = 0

    x_start, x_end = 80, 90
    y_search1, y_search2 = 135, 138
    y_search_for_bird = 101

    time.sleep(3)

    while not keyboard.is_pressed('q'):
        screenshot = np.array(gui.screenshot(region=(x, y, width, height)))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        bg_color = get_pixel(screenshot, 100, 100)

        for i in reversed(range(x_start, x_end)):
            if np.any(screenshot[y_search1, i] != bg_color) or np.any(screenshot[y_search2, i] != bg_color):
                keyboard.press('up')
                jumping_time = time.time()
                break
            if np.any(screenshot[y_search_for_bird, i] != bg_color):
                keyboard.press("down")
                time.sleep(0.4)
                keyboard.release("down")
                break

        interval_time = jumping_time - last_jumping_time

        if last_interval_time and math.floor(interval_time) != math.floor(last_interval_time):
            x_end += 4
            x_end = min(x_end, width)

        last_jumping_time = jumping_time
        last_interval_time = interval_time


start()
