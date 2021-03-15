import matplotlib.pylab as plt
import cv2
import numpy as np
import sys
import os
import datetime
import time
import math

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    #channel_count = img.shape[2]
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def calculate_line_angle(x1, y1, x2, y2):
    y = (y2 - y1)**2
    x = (x2 - x1)**2
    try:
        theta = math.atan(math.sqrt(y)/math.sqrt(x))
    except:
        x = 0.001
        theta = math.atan(math.sqrt(y)/math.sqrt(x))

    theta_deg = math.degrees(theta)
    return theta_deg 



def draw_the_lines(img, lines):
    img = np.copy(img)
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    for line in lines:
        for x1, y1, x2, y2 in line:
            theta = calculate_line_angle(x1,y1,x2,y2)
            if theta > 5 and theta < 70:
                cv2.line(blank_image, (x1,y1), (x2,y2), (0, 255, 0), thickness=5)

    img = cv2.addWeighted(img, 0.8, blank_image, 1, 0.0)
    return img


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
        (width/2.5, height*0.7),
        (width/1.5, height*0.7),
        (width*0.9, height)
    ]
    image_brightened = increase_brightness(image)
    grey_image = cv2.cvtColor(image_brightened, cv2.COLOR_RGB2GRAY)
    gaussian_image = cv2.GaussianBlur(grey_image, (5, 5), 0)
    # kernel = np.ones((5, 5), np.uint8)
    # opening = cv2.morphologyEx(gaussian_image, cv2.MORPH_OPEN, kernel)  # Open (erode, then dilate)
    edges = cv2.Canny(gaussian_image,50,150)
    cropped_image = region_of_interest(edges,
                    np.array([region_of_interest_vertices], np.int32),)

    if save_frame:
        save_image(grey_image, frame_count, "greyscale")
        save_image(image_brightened, frame_count, "brightened")
        save_image(edges, frame_count, "canny")
        # save_image(opening, frame_count, "opening")
        save_image(gaussian_image, frame_count, "gauss")
        save_image(cropped_image, frame_count, "cropped_image")

    lines = cv2.HoughLinesP(cropped_image,
                            rho=1,
                            theta=np.pi/180,
                            threshold=90,
                            lines=np.array([]),
                            minLineLength=50,
                            maxLineGap=90)

    if lines is not None:
        image_with_lines = draw_the_lines(image, lines)
        return image_with_lines

    return image


######### MAIN PROGRAM ########
try: 
    video_title = sys.argv[1] 
    runtime = int(sys.argv[2])
    test_sample_frame = int(sys.argv[3])
except:
    # Test Data
    video_title =  'fineB_day_none_low_10'
    runtime = 30
    test_sample_frame = None



# set file paths and directories
dirname = os.path.dirname(__file__)
video_directory = os.path.join(dirname, 'video_input')
video_path = os.path.join(video_directory, video_title + ".mp4")
run_name = video_title + "/{0}/".format(datetime.datetime.utcnow().strftime("%s"))
output_path = os.path.join("output/" + run_name)
os.makedirs(output_path)    

# create video capture
cap = cv2.VideoCapture(video_path)

# Initialise frame count 
frame_count = 0

# while the video plays or if we have set a runtime
while cap.isOpened() and (frame_count/cv2.cv2.CAP_PROP_FPS)<runtime:
    ret, frame = cap.read()
    key=cv2.waitKey(1)
    save_frame = False

    if frame is not None:
        frame_count+=1

        if key == 27:
            break
    
        elif key == 32 or (frame_count%20 == 0 and frame_count<=101):
            save_frame = True

        frame = process(frame, save_frame, frame_count)    
        cv2.imshow('frame', frame)

        if save_frame:
            save_image(frame, frame_count, "frame")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()