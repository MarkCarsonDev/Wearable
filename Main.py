# Libraries
import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw

# Local classes
import Webcam
import RegionDetection 

def main():
    cam = cv.VideoCapture(0)
    run = True

    while (run):
        im_cv = Webcam.get_image(cam, mirror=True)
        #im_cv = cv.resize(im_cv, (0, 0), fx=0.5, fy=0.5)

        match = RegionDetection.getMatchBounds(im_cv, 'face')
        
        x = match[0]
        y = match[1]
        w = match[2]
        h = match[3]

        cv.rectangle(im_cv, (x, y), (x+w, y+h), (255, 0, 255), 2)
    
        sV = 0.5

        #im_cv = cv.resize(im_cv, (0, 0), fx=sV, fy=sV)

        color = (255, 255, 255)
        shirtCenter = (0, 0)

        # x = int(x * sV)
        # y = int(y * sV)
        # w = int(w * sV)
        # h = int(h * sV)

        shirtCenter = int((2 * x + w) / 2), min(y + 2 * h, im_cv.shape[0])

        shirtCorners = [(max(int(shirtCenter[0] - 2.5 * w), 0), max(y+h, 0)), (min(int(shirtCenter[0] + 2.5 * w), im_cv.shape[1]), min(shirtCenter[0] + 3 * h, im_cv.shape[0]))]

        cv.rectangle(im_cv, (shirtCenter[0]-1, shirtCenter[1]-1), (shirtCenter[0]+1, shirtCenter[1]+1), (255, 255, 0), 5)
        cv.rectangle(im_cv, shirtCorners[0], shirtCorners[1], (255, 255, 0), 5)
    
        im_cv = cv.cvtColor(im_cv, cv.COLOR_BGR2RGB) 
        im_cv_hsv = cv.cvtColor(im_cv, cv.COLOR_BGR2HSV_FULL)

        lightest_pixel = (0, 0, 0)
        for o in range(shirtCorners[1][0] - shirtCorners[0][0]):
            for p in range(shirtCorners[1][1] - shirtCorners[0][1]):
                if im_cv_hsv[shirtCorners[0][0] + o - 1][shirtCorners[0][1] + p - 1][2] > lightest_pixel[2]:
                    print(lightest_pixel[2])
                    lightest_pixel = (o, p, im_cv_hsv[shirtCorners[0][0] + o][shirtCorners[0][1] + p][2])

        cv.rectangle(im_cv, (lightest_pixel[0]-1, lightest_pixel[1]-1), (lightest_pixel[0]+1, lightest_pixel[1]+1), (0, 255, 0), 7)

        im_pil = Image.fromarray(im_cv)

        ImageDraw.floodfill(im_pil, shirtCenter, color, thresh=85)

        im_np = np.asarray(im_pil)
        im_cv = cv.cvtColor(im_np, cv.COLOR_RGB2BGR)

        
        k = cv.waitKey(30) & 0xff
        if k==27:
            run = False
            break


        cv.imshow('bruh', im_cv)

    cam.release()

def shirtMask(im_cv, shirtColor):

    # Convert to HSV
    hsv = cv.cvtColor(im_cv, cv.COLOR_BGR2HSV)

    # Define lower and uppper limits of what we call "white-ish"
    sensitivity = 19
    lower_white = np.array([0, 0, 255 - sensitivity])
    upper_white = np.array([255, sensitivity, 255])

    # Create mask to only select white
    mask = cv.inRange(hsv, lower_white, upper_white)

    # Draw new rectangular mask on old mask that is black inside the rectangle and white outside the rectangle
    x,y,w,h = 33,100,430,550
    mask2 = mask.copy()
    cv.rectangle(mask2, (x,y), (x+w,y+h), 0, -1)

    # Change image to grey where we found white for combined mask
    result = im_cv.copy()
    result[mask2 > 0] = (170, 170, 170)

    # save results
    cv.imwrite('4animals_mask.jpg', mask)
    cv.imwrite('4animals_mask2.jpg', mask2)
    cv.imwrite('4animals_result.jpg', result)

    cv.imshow('mask', mask)
    cv.imshow('mask2', mask2 )
    cv.imshow('result', result)
    cv.waitKey(0)
    cv.destroyAllWindows()

    

if __name__ == "__main__":
    main()
