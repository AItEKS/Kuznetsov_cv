import numpy as np
from scipy.ndimage import label
from skimage.morphology import binary_erosion, binary_dilation


def neighbours8(y, x):
    return (y, x - 1), (y - 1, x), (y, x + 1), (y + 1, x), (y - 1, x - 1), (y - 1, x + 1), (y + 1, x - 1), (y + 1, x + 1)


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