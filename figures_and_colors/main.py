import cv2
import numpy as np
from collections import defaultdict

def get_shades(img):
    c = np.unique(img[:, :])
    colors = []
    e = np.diff(c).mean()
    prev_color = -1
    a = []

    for i in c:
        if prev_color == -1:
            a.append(i)
        elif np.abs(i - prev_color) >= e:
            mean = np.mean(a)
            if mean != 0.0:
                colors.append(mean)
            a = [i]
        else:
            a.append(i)
        prev_color = i

    colors.append(np.mean(a))
    return colors


img = cv2.imread('balls_and_rects.png', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
shades = get_shades(gray)
gray_blurred = cv2.blur(gray, (2, 2))

detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=13, minRadius=1, maxRadius=50)

circle_count = 0
circle_shades = defaultdict(float)
if detected_circles is not None:
    detected_circles = np.uint16(np.around(detected_circles))

    for pt in detected_circles[0, :]:
        circle_count += 1
        a, b, r = pt[0], pt[1], pt[2]
        mask = np.zeros_like(img)
        cv2.circle(mask, (a, b), r, (255, 255, 255), -1)

        hsv_img = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)
        object_color_hsv = np.mean(hsv_img, axis=(0, 1))
        hue = object_color_hsv[0]
        for i in shades:
            if i == hue:
                circle_shades[i] += 1

        cv2.circle(img, (a, b), r, (0, 255, 0), 2)
        cv2.circle(img, (a, b), 1, (0, 0, 255), 1)

cv2.imshow("Detected Circle", img)
cv2.waitKey(0)

img = cv2.imread('balls_and_rects.png', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = cv2.GaussianBlur(gray, (7, 7), 0)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
gray = cv2.dilate(gray, kernel, iterations=1)

edges = cv2.Canny(gray, 3, 5)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

rectangle_count = 0
rectangle_shades = defaultdict(float)
for contour in contours:
    epsilon = 0.03 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    if len(approx) == 4:
        rectangle_count += 1
        mask = np.zeros_like(img)
        cv2.drawContours(mask, [approx], 0, (255, 255, 255), -1)

        mask_single_channel = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        moments = cv2.moments(mask_single_channel)
        a, b = int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00'])
        hsv_img = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)
        object_color_hsv = np.mean(hsv_img, axis=(0, 1))
        hue = object_color_hsv[0]
        for i in shades:
            if i == hue:
                rectangle_shades[i] += 1

        cv2.drawContours(img, [approx], 0, (255, 0, 0), 1)

cv2.imshow("Detected Rectangles", img)
cv2.waitKey(0)

print("Total number of rectangles:", rectangle_count)
print("Rectangles by shades:", rectangle_shades)

print("Total number of circles:", circle_count)
print("Circles by shades:", circle_shades)

print("Total number of figures:", rectangle_count + circle_count)