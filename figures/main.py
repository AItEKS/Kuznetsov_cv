import numpy as np
from scipy.ndimage import label
from skimage.morphology import binary_erosion, binary_dilation


def neighbours8(y, x):
    return (y, x - 1), (y - 1, x), (y, x + 1), (y + 1, x), (y - 1, x - 1), (y - 1, x + 1), (y + 1, x - 1), (y + 1, x + 1)


image = np.load("ps.npy.txt")

structure_1 = np.array([[1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0]])

structure_2 = np.array([[1, 1, 1, 1, 0, 0],
                   [1, 1, 1, 1, 0, 0],
                   [0, 0, 1, 1, 0, 0],
                   [0, 0, 1, 1, 0, 0],
                   [1, 1, 1, 1, 0, 0],
                   [1, 1, 1, 1, 0, 0]])

structure_3 = np.array([[1, 1, 0, 0, 1, 1],
                   [1, 1, 0, 0, 1, 1],
                   [1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0]])

structure_4 = np.array([[1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1],
                   [1, 1, 0, 0, 1, 1],
                   [1, 1, 0, 0, 1, 1],
                   [0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0]])

structure_5 = np.array([[1, 1, 1, 1, 0, 0],
                   [1, 1, 1, 1, 0, 0],
                   [1, 1, 0, 0, 0, 0],
                   [1, 1, 0, 0, 0, 0],
                   [1, 1, 1, 1, 0, 0],
                   [1, 1, 1, 1, 0, 0]])


labeled = label(image)[0]

print(f'Количество фигур: {labeled.max()}')

ans = binary_dilation(binary_erosion(image, structure_1), structure_1)
print(f'Тип 1: {label(ans)[0].max()}')

image -= ans

ans = binary_dilation(binary_erosion(image, structure_2), structure_2)
print(f'Тип 2: {label(ans)[0].max()}')

image -= ans

ans = binary_dilation(binary_erosion(image, structure_3), structure_3)
print(f'Тип 3: {label(ans)[0].max()}')

image -= ans

ans = binary_dilation(binary_erosion(image, structure_4), structure_4)
print(f'Тип 4: {label(ans)[0].max()}')

image -= ans

ans = binary_dilation(binary_erosion(image, structure_5), structure_5)
print(f'Тип 5: {label(ans)[0].max()}')