import matplotlib.pyplot as plt
import pyautogui as gui
import keyboard
import cv2
import numpy as np
import time


def start():
    x, y, width, height = 710, 180, 550, 350

    bg_color = [247, 247, 247]

    x_start, x_end = 60, 110
    y_search1, y_search2 = 132, 138
    y_search_for_bird = 102

    time.sleep(3)
    keyboard.press('up')
    keyboard.release('up')

    while not keyboard.is_pressed('q'):
        screenshot = gui.screenshot(region=(x, y, width, height))
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        for i in reversed(range(x_start, x_end)):
            if np.any(screenshot[y_search1, i] != bg_color) or np.any(screenshot[y_search2, i] != bg_color):
                new_screenshot = gui.screenshot(region=(735, 310, 65, 13))
                new_screenshot = cv2.cvtColor(np.array(new_screenshot), cv2.COLOR_RGB2BGR)

                while np.any(new_screenshot != bg_color):
                    keyboard.press('up')

                    new_screenshot = gui.screenshot(region=(735, 310, 65, 13))
                    new_screenshot = cv2.cvtColor(np.array(new_screenshot), cv2.COLOR_RGB2BGR)

                    # plt.imshow(new_screenshot)
                    # plt.show()

                keyboard.press('down')
                keyboard.release('down')

                keyboard.press('down')
                keyboard.release('down')

                break

            if np.any(screenshot[y_search_for_bird, i] != bg_color):
                keyboard.press("down")
                time.sleep(0.5)
                keyboard.release("down")
                break


start()
