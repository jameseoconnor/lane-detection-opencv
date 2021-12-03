# import matplotlib.pylab as plt
# import cv2
# import numpy as np

# def region_of_interest(img, vertices):
#     mask = np.zeros_like(img)
#     #channel_count = img.shape[2]
#     match_mask_color = 255
#     cv2.fillPoly(mask, vertices, match_mask_color)
#     masked_image = cv2.bitwise_and(img, mask)
#     return masked_image

# def drow_the_lines(img, lines):
#     img = np.copy(img)
#     blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

#     for line in lines:
#         for x1, y1, x2, y2 in line:
#             cv2.line(blank_image, (x1,y1), (x2,y2), (0, 255, 0), thickness=5)

#     img = cv2.addWeighted(img, 0.8, blank_image, 1, 0.0)
#     return img

# # https://www.agriland.ie/farming-news/range-of-measures-announced-on-vehicle-tests-and-driving-licences/
# image = cv2.imread('road.jpg')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# print(image.shape)
# height = image.shape[0]
# width = image.shape[1]
# region_of_interest_vertices = [
#     (0, height),
#     (width/2, height/3),
#     (width, height)
# ]
# gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
# canny_image = cv2.Canny(gray_image, 100, 200)
# cropped_image = region_of_interest(canny_image,
#                 np.array([region_of_interest_vertices], np.int32),)
# lines = cv2.HoughLinesP(cropped_image,
#                         rho=6,
#                         theta=np.pi/180,
#                         threshold=160,
#                         lines=np.array([]),
#                         minLineLength=10,
#                         maxLineGap=25)
# image_with_lines = drow_the_lines(image, lines)

# plt.imshow(cropped_image)
# plt.show()
# plt.imshow(image_with_lines)
# plt.show()

import matplotlib.pylab as plt
import cv2
import numpy as np

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

def set_directories(video_title):
    dirname = os.path.dirname(__file__)
    video_directory = os.path.join(dirname, 'video_input')
    video_path = os.path.join(video_directory, video_title + ".mp4")
    run_name = video_title + "/{0}/".format(datetime.datetime.utcnow().strftime("%s"))
    output_path = os.path.join("output/" + run_name)
    os.makedirs(output_path)

    return video_path, output_path

    

# image = cv2.imread('road.jpg')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def process(image):
    print(image.shape)
    height = image.shape[0]
    width = image.shape[1]
    region_of_interest_vertices = [
        (0, height),
        (width/2, height/2),
        (width, height)
    ]
    gray_image = grey(image)
    gaussian_image = gauss(image)
    canny_image = canny(image)
    cropped_image = region_of_interest(canny_image,
                    np.array([region_of_interest_vertices], np.int32),)
    lines = cv2.HoughLinesP(cropped_image,
                            rho=2,
                            theta=np.pi/180,
                            threshold=50,
                            lines=np.array([]),
                            minLineLength=40,
                            maxLineGap=100)
    if lines is not None:
        image_with_lines = drow_the_lines(image, lines)
        return image_with_lines
    
    return image


try: 
    video_title = sys.argv[1] 
    runtime = int(sys.argv[2])
    test_sample_frame = int(sys.argv[3])
except:
    # Test Data
    video_title =  'default'

    # Runtime of the video in seconds
    runtime = 30
    test_sample_frame = None

# Initialise frame count 
frame_count = 0

# Setup directores for output 
video_path, output_path = set_directories(video_title)

# create video capture
cap = cv2.VideoCapture(video_path)

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