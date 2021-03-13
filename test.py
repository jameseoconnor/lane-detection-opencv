import numpy as np
from PIL import Image
# result = (4*14 + 4) + (24+16)*4 + 36

# sobel_h = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
# sobel_v = [-1, -2, -1, 0, 0, 0, 1, 2, 1]

# sobel_h = np.array(sobel_h).reshape(3,3)
# sobel_v = np.array(sobel_v).reshape(3,3)
# print(sobel_h, "\n", sobel_v)

image_size = 50
blank_image = np.random.rand(image_size,image_size)*256
blank_image = np.round(blank_image, 0)

img = Image.fromarray(blank_image, 'RGB')
# img.save('my.png')
img.show()
