import matplotlib.pylab as plt 
import cv2
import numpy as np 


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    # channels_count = img.shape[2]
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

# https://www.agriland.ie/farming-news/range-of-measures-announced-on-vehicle-tests-and-driving-licences/
image = cv2.imread('road.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

height = image.shape[0]
width = image.shape[1]

region_of_interest_vertices = [
    (0, height),
    (width/2, height/3),
    (width, height)
]

grey_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
canny_iamge = cv2.Canny(grey_image, 100, 200)
cropped_image = region_of_interest(canny_iamge, 
                    np.array([region_of_interest_vertices],  np.int32),)




plt.imshow(cropped_image)
plt.show()
