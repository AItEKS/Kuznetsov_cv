import cv2
import numpy as np

img = cv2.imread('balls_and_rects.png', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_blurred = cv2.blur(gray, (2, 2))

detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=13, minRadius=1, maxRadius=50)

circle_count = 0
circle_colors = {'red': 0, 'green': 0, 'blue': 0}
if detected_circles is not None:
    detected_circles = np.uint16(np.around(detected_circles))

    for pt in detected_circles[0, :]:
        circle_count += 1
        a, b, r = pt[0], pt[1], pt[2]
        mask = np.zeros_like(img)
        cv2.circle(mask, (a, b), r, (255, 255, 255), -1)
        circle_color = img[b - r:b + r, a - r:a + r, :]
        circle_color = cv2.mean(circle_color)

        if circle_color[0] > circle_color[1] and circle_color[0] > circle_color[2]:
            circle_colors['red'] += 1
        elif circle_color[1] > circle_color[0] and circle_color[1] > circle_color[2]:
            circle_colors['green'] += 1
        else:
            circle_colors['blue'] += 1

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
rectangle_colors = {'red': 0, 'green': 0, 'blue': 0}
for contour in contours:
    epsilon = 0.03 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    if len(approx) == 4:
        rectangle_count += 1
        mask = np.zeros_like(img)
        cv2.drawContours(mask, [approx], 0, (255, 255, 255), -1)
        rectangle_color = img[mask.astype('bool')]
        rectangle_color = cv2.mean(rectangle_color)

        if rectangle_color[0] > rectangle_color[1] and rectangle_color[0] > rectangle_color[2]:
            rectangle_colors['red'] += 1
        elif rectangle_color[1] > rectangle_color[0] and rectangle_color[1] > rectangle_color[2]:
            rectangle_colors['green'] += 1
        else:
            rectangle_colors['blue'] += 1

        cv2.drawContours(img, [approx], 0, (255, 0, 0), 1)

cv2.imshow("Detected Rectangles", img)
cv2.waitKey(0)

print("Number of rectangles:")
print("Red:", rectangle_colors['red'])
print("Green:", rectangle_colors['green'])
print("Blue:", rectangle_colors['blue'])
print("Total:", rectangle_count)

print("Number of circles:")
print("Red:", circle_colors['red'])
print("Green:", circle_colors['green'])
print("Blue:", circle_colors['blue'])
print("Total:", circle_count)

print("Total number of figures:", rectangle_count + circle_count)