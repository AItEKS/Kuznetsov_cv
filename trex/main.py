import pyautogui as gui
import keyboard
from PIL import ImageGrab
import time
import math


def get_pixel(image, x, y):
    px = image.load()
    width, height = image.size
    if 0 <= x < width and 0 <= y < height:
        return px[x, y]
    else:
        return None


def start():
    x, y, width, height = 710, 180, 1260, 350
    jumping_time = 0
    last_jumping_time = 0
    last_interval_time = 0

    time.sleep(3)

    while True:
        if keyboard.is_pressed('q'):
            break

        sct_img = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        bg_color = get_pixel(sct_img, 100, 100)

        x_start, x_end = 80, 95
        y_search1, y_search2 = 135, 138
        y_search_for_bird = 103

        for i in reversed(range(x_start, x_end)):
            if get_pixel(sct_img, i, y_search1) != bg_color or get_pixel(sct_img, i, y_search2) != bg_color:
                keyboard.press('up')
                jumping_time = time.time()
                break
            if get_pixel(sct_img, i, y_search_for_bird) != bg_color:
                keyboard.press("down")
                time.sleep(0.3)
                keyboard.release("down")
                break

        interval_time = jumping_time - last_jumping_time

        if last_interval_time != 0 and math.floor(interval_time) != math.floor(last_interval_time):
            x_end += 2
            if x_end >= width:
                x_end = width

        last_jumping_time = jumping_time
        last_interval_time = interval_time


start()
