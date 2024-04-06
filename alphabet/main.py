import numpy as np
from skimage.measure import regionprops
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.filters import threshold_otsu
from collections import defaultdict
from pathlib import Path


def hist(arr):
    result = np.zeros(256)
    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            result[arr[y, x]] += 1
    return result


def fil_fac(arr):
    return np.sum(arr) / arr.size


def count_hole(region):
    labeled = label(np.logical_not(region.image))
    regions = regionprops(labeled)
    holes = 0
    for region in regions:
        coords = np.where(labeled == region.label)
        bound = True
        for y, x in zip(*coords):
            if y == 0 or x == 0 or y == labeled.shape[0] - 1 or x == labeled.shape[1] - 1:
                bound = False
        holes += bound
    return holes


def has_line(arr, width = 3):
    return width <= np.sum(arr.mean(0) == 1.0)


def recognize(region):
    if fil_fac(region.image) == 1.0:
        return "-"

    else:
        holes = count_hole(region)
        if holes == 2:
            if has_line(region.image):
                return "B"
            else:
                return "8"
        elif holes == 1:
            ny, nx = (region.centroid_local[0] / region.image.shape[0], region.centroid_local[1] / region.image.shape[1])
            if np.isclose(ny, nx, 0.09):
                if has_line(region.image, 3):
                    return "P"
                else:
                    return "0"
            elif has_line(region.image, 3):
                return "D"
            else:
                return "A"
        else:
            if has_line(region.image):
                return "1"
            else:
                eccen = region.eccentricity
                frame = region.image
                frame[0, :] = 1
                frame[-1, :] = 1
                frame[:, 0] = 1
                frame[:, -1] = 1
                holes = count_hole(region)

                if eccen < 0.4:
                    return "*"

                else:
                    match holes:
                        case 2: return "/"
                        case 4: return "A"
                        case _: return "W"
    return "_"


image = plt.imread("symbols.png").mean(2)
image[image > 0] = 1
regions = regionprops(label(image))
symbols = len(regions)

result = defaultdict(lambda: 0)
path = Path(".") / "result"
path.mkdir(exist_ok=True)

plt.figure()
for i, region in enumerate(regions):
    symbol = recognize(region)
    # plt.clf()
    # plt.title(f"{symbol=}")
    # plt.imshow(region.image)
    # plt.tight_layout()
    # plt.savefig(path / f"{i}.png")
    result[symbol] += 1

print(result)
