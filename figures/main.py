import numpy as np
from scipy.ndimage import label
from skimage.morphology import binary_erosion, binary_dilation


def neighbours8(y, x):
    return (y, x - 1), (y - 1, x), (y, x + 1), (y + 1, x), (y - 1, x - 1), (y - 1, x + 1), (y + 1, x - 1), (y + 1, x + 1)


def get_boundaries(LB, label=1):
    pos = np.where(LB == label)
    bounds = []
    for y, x in zip(*pos):
        for yn, xn in neighbours8(y, x):
            if yn < 0 or xn < 0 or yn >= LB.shape[0] or xn >= LB.shape[1] or LB[yn, xn] == 0:
                bounds.append((y, x))
                break
    return bounds


def get_shape(bounds):
    y_min, x_min = bounds[0][0], bounds[0][1]
    LB = np.zeros((6, 6))
    for y, x in bounds:
        LB[y - y_min, x - x_min] = 1
    return LB


image = np.load("ps.npy.txt")

type_1 = np.array([[1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0]])

type_2 = np.array([[1, 1, 1, 1, 0, 0],
                  [1, 1, 1, 1, 0, 0],
                  [0, 0, 1, 1, 0, 0],
                  [0, 0, 1, 1, 0, 0],
                  [1, 1, 1, 1, 0, 0],
                  [1, 1, 1, 1, 0, 0]])

type_3 = np.array([[1, 1, 0, 0, 1, 1],
                  [1, 1, 0, 0, 1, 1],
                  [1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0]])

type_4 = np.array([[1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1],
                  [1, 1, 0, 0, 1, 1],
                  [1, 1, 0, 0, 1, 1],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0]])

type_5 = np.array([[1, 1, 1, 1, 0, 0],
                  [1, 1, 1, 1, 0, 0],
                  [1, 1, 0, 0, 0, 0],
                  [1, 1, 0, 0, 0, 0],
                  [1, 1, 1, 1, 0, 0],
                  [1, 1, 1, 1, 0, 0]])


labeled = label(image)[0]

print(f'Количество фигур: {labeled.max()}')

ans = binary_dilation(binary_erosion(image, type_1), type_1)
print(f'Тип 1: {label(ans)[0].max()}')

image -= ans

ans = binary_dilation(binary_erosion(image, type_2), type_2)
print(f'Тип 2: {label(ans)[0].max()}')

image -= ans

ans = binary_dilation(binary_erosion(image, type_3), type_3)
print(f'Тип 3: {label(ans)[0].max()}')

image -= ans

ans = binary_dilation(binary_erosion(image, type_4), type_4)
print(f'Тип 4: {label(ans)[0].max()}')

image -= ans

ans = binary_dilation(binary_erosion(image, type_5), type_5)
print(f'Тип 5: {label(ans)[0].max()}')
