import cv2
import zmq
import numpy as np


def lower_update(value):
    global lower
    lower = value


def upper_update(value):
    global upper
    upper = value


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped


cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
cap.set(cv2.CAP_PROP_EXPOSURE, 5)

lower = 100
upper = 200

cv2.createTrackbar("Lower", "Mask", lower, 255, lower_update)
cv2.createTrackbar("Upper", "Mask", upper, 255, upper_update)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
port = 5055
socket.connect(f"tcp://192.168.0.113:{port}")

while True:
    bts = socket.recv()
    arr = np.frombuffer(bts, np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    mask = cv2.Canny(gray, lower, upper)

    cnts, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(cnts)):
        cv2.drawContours(frame, cnts, i, (0, 0, 0), 1)

    blue_points = []
    for cnt in cnts:
        epsilon = 0.1 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        for point in approx:
            cv2.circle(frame, tuple(point[0]), 2, (255, 0, 0), -1)
            blue_points.append(tuple(point[0]))

    if len(blue_points) >= 4:
        pts1 = np.float32([[235, 235], [450, 235],
                           [450, 300], [235, 300]])

        pts2 = np.float32(blue_points)[:-4]

        M = cv2.getPerspectiveTransform(pts1, pts2)

        text = "Hello World"
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (100, 100)
        fontScale = 1.5
        color = (125, 255, 125)
        thickness = 5

        warped_text = cv2.warpPerspective(np.full((200, 400, 3), 255, dtype=np.uint8), M, (400, 200))
        cv2.putText(warped_text, text, org, font, fontScale, color, thickness, cv2.LINE_AA)

        roi = frame[100:300, 100:500]
        roi_bg = cv2.bitwise_and(roi, cv2.bitwise_not(warped_text))
        roi_fg = cv2.bitwise_and(warped_text, warped_text)
        frame[100:300, 100:500] = roi_bg + roi_fg

    cv2.imshow("Image", frame)
    cv2.imshow('Mask', mask)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()