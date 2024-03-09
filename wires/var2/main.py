import numpy as np
from skimage.measure import label
from skimage.morphology import binary_opening, binary_erosion

struct = np.array([[0, 1, 0],
                   [0, 1, 0],
                   [0, 1, 0]])

image = np.load("wires4.npy.txt")
image_lb = label(image)

for i in range(1, image_lb.max() + 1):
    im = binary_erosion(image_lb == i, struct)
    max_ind = np.max(label(im))
    match max_ind:
        case 1:
            print(f"Провод {i} целый")
        case 2:
            print(f"Провод {i} не провод")
        case 3:
            print(f"Провод {i} разбит на", max_ind, "частей")