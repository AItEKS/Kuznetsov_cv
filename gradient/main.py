import numpy as np
import matplotlib.pyplot as plt


def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1


color1 = np.array([255, 100, 0])
color2 = np.array([0, 100, 255])
size = 100
image = np.zeros((size, size, 3), dtype="uint8")

x = np.linspace(0, 1, size)
y = np.linspace(0, 1, size)
xg, yg = np.meshgrid(x, y)
colors = lerp(color2, color1, ((xg + yg) / 2)[..., np.newaxis])
image[:, :, :] = colors.astype(np.uint8)

plt.figure(1)
plt.imshow(image)
plt.show()
