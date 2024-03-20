import numpy as np
from scipy.ndimage import binary_opening, label


def count_objects(image, structure):
    opened_image = binary_opening(image, structure)
    labeled_image, num_objects = label(opened_image)
    return num_objects


image = np.load('ps.npy.txt')

structures = [
    np.array([[1, 1],
              [1, 0],
              [1, 1]]),

    np.array([[1, 1, 1],
              [1, 1, 1]]),

    np.array([[1, 1, 1],
              [1, 0, 1]])
]

total_objects = 0
objects_count = []

for structure in structures:
    num_objects = count_objects(image, structure)
    total_objects += num_objects
    objects_count.append(num_objects)

print(f"Общее количество всех объектов в файле: {total_objects}")
print(f"Количество объектов для каждого вида по отдельности: {objects_count}")
