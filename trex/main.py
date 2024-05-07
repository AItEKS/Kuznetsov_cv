import pyautogui as gui
import keyboard
import cv2
import numpy as np
import time
import math
import matplotlib.pyplot as plt


def get_pixel(image, x, y):
    if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
        return image[y, x]
    else:
        return None


def start():
    x, y, width, height = 710, 180, 550, 350
    jumping_time = 0
    last_jumping_time = 0
    last_interval_time = 0

    x_start, x_end = 76, 85
    y_search1, y_search2 = 115, 135
    y_search_for_bird = 99

    time.sleep(3)
    keyboard.press('up')
    keyboard.release('up')

    while not keyboard.is_pressed('q'):
        screenshot = gui.screenshot(region=(x, y, width, height))
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        bg_color = get_pixel(screenshot, 100, 100)

        for i in reversed(range(x_start, x_end)):
            if np.any(screenshot[y_search1, i] != bg_color) or np.any(screenshot[y_search2, i] != bg_color):
                keyboard.press('up')
                jumping_time = time.time()
                # plt.imshow(screenshot)
                # plt.show()
                if x_start < 85:
                    x_start += 3

                break

            if np.any(screenshot[y_search_for_bird, i] != bg_color):
                keyboard.press("down")
                time.sleep(0.5)
                keyboard.release("down")
                # plt.imshow(screenshot)
                # plt.show()
                if x_end < 95:
                    x_end += 2

                break

        interval_time = jumping_time - last_jumping_time

        if last_interval_time and math.floor(interval_time) != math.floor(last_interval_time):
            x_end += 2
            x_end = min(x_end, width)

        last_jumping_time = jumping_time
        last_interval_time = interval_time

        if np.all(screenshot[90, (235, 262)] == [83, 83, 83]):
            jumping_time = 0
            last_jumping_time = 0
            last_interval_time = 0
            x_start, x_end = 76, 85

            keyboard.press('up')
            keyboard.release('up')



start()
