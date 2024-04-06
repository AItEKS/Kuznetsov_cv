import cv2
from scipy.spatial import distance

general_count = 0

for i in range(1, 13):
    img = cv2.imread(f"images/img ({i}).jpg")
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (7, 7), 0)
    _, thresh = cv2.threshold(image, 120, 255, 0)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    pencil_number = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        points = cv2.boxPoints(cv2.minAreaRect(cnt))
        w_euc = distance.euclidean(points[0], points[1])
        h_euc = distance.euclidean(points[0], points[3])
        if (h_euc > 3 * w_euc and h_euc > 900) or (w_euc > 3 * h_euc and w_euc > 900):
            pencil_number += 1
            general_count += 1

    print(f"Количество карандашей на {i} изображении: {pencil_number}")

print(f"Суммарное количество всех карандашей: {general_count}")