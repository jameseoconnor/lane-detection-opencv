import matplotlib.pylab as plt
import cv2
import numpy as np
import sys
import os
import datetime
import time


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    #channel_count = img.shape[2]
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def drow_the_lines(img, lines):
    img = np.copy(img)
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(blank_image, (x1,y1), (x2,y2), (0, 255, 0), thickness=5)

    img = cv2.addWeighted(img, 0.8, blank_image, 1, 0.0)
    return img


def grey(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


def gauss(image):
    return cv2.GaussianBlur(image, (5, 5), 0)


def canny(image):
    edges = cv2.Canny(image,50,150)
    return edges

def save_image(image, frame_count, tag):
    save_folder = output_path + format(str(frame_count))
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    save_location = save_folder + f"/{tag}.jpg"
    cv2.imwrite(save_location, image)

def process(image, save_frame, frame_count):
    print(image.shape)
    height = image.shape[0]
    width = image.shape[1]
    region_of_interest_vertices = [
        (0, height),
        (width/2, height*0.7),
        (width, height)
    ]
    grey_image = grey(image)
    gaussian_image = gauss(grey_image)
    canny_image = canny(gaussian_image)
    cropped_image = region_of_interest(canny_image,
                    np.array([region_of_interest_vertices], np.int32),)

    if save_frame:
        save_image(grey_image, frame_count, "greyscale")
        save_image(canny_image, frame_count, "canny")
        save_image(cropped_image, frame_count, "cropped_image")

    lines = cv2.HoughLinesP(cropped_image,
                            rho=2,
                            theta=np.pi/180,
                            threshold=80,
                            lines=np.array([]),
                            minLineLength=20,
                            maxLineGap=200)

    if lines is not None:
        image_with_lines = drow_the_lines(image, lines)
        return image_with_lines

    return image



# Main Program
try: 
    video_title = sys.argv[1] 
except:
    # Test
    video_title =  'scenario1_clear_urban'


dirname = os.path.dirname(__file__)
video_directory = os.path.join(dirname, 'video_input')

video_path = os.path.join(video_directory, video_title + ".mp4")
run_name = video_title + "/{0}/".format(datetime.datetime.utcnow().strftime("%s"))

output_path = os.path.join("output/" + run_name)
os.makedirs(output_path)    

cap = cv2.VideoCapture(video_path)
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    key=cv2.waitKey(1)
    save_frame = False

    if key == 27:
        break
    elif key == 32:
        save_frame = True

    if frame is not None:
        frame_count+=1
        frame = process(frame, save_frame, frame_count)    
        cv2.imshow('frame', frame)

        if save_frame:
            save_image(frame, frame_count, "frame")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        save_frame = False

cap.release()
cv2.destroyAllWindows()