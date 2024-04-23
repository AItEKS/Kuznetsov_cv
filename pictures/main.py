import cv2
import numpy as np

capture = cv2.VideoCapture('pictures.avi')

my_image = 0
while True:
    success, img = capture.read()
    if success:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 50, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 7:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(img, 127, 255, 0)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # for cnt in contours:
            #     (x, y), radius = cv2.minEnclosingCircle(cnt)
            #     center = (int(x), int(y))
            #     radius = int(radius)
            #     cv2.circle(img, center, radius, (0, 255, 0), 2)
            if len(contours) == 1:
                my_image += 1
                # cv2.imshow('detected circles', img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
    else:
        break

capture.release()
print(my_image)

# Ответ: 46
