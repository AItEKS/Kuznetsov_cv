import numpy as np
from skimage.morphology import binary_opening

struct = np.array([[0, 1, 0],
                   [0, 1, 0],
                   [0, 1, 0]])

image = np.load("wires5.npy.txt")
opened_image = binary_opening(image, struct)

parts_count = set()

for row in range(opened_image.shape[0]):
    if opened_image[row, 0] != 0:
        parts = sum(1 for pixel in opened_image[row] if pixel == 0)
        parts_count.add(parts)

for idx, parts in enumerate(parts_count, start=1):
    print(f"Провод {idx}: {parts + 1} часть")
