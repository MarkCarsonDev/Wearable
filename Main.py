# Libraries
import cv2 as cv
import numpy as np


# Local classes
import Webcam
import RegionDetection 

def main():
    cam = cv.VideoCapture(0)
    run = True

    while (run):
        im_cv = Webcam.get_image(cam, mirror=True)
        im_cv = cv.resize(im_cv, (0, 0), fx=0.5, fy=0.5)

        match = RegionDetection.getMatchBounds(im_cv, 'face')
        
        x = match[0]
        y = match[1]
        w = match[2]
        h = match[3]

        cv.rectangle(im_cv, (x, y), (x+w, y+h), (255, 0, 255), 1)
    
        sV = 1

        im_cv = cv.resize(im_cv, (0, 0), fx=sV, fy=sV)
        shirtCenter = (0, 0)

        x = int(x * sV)
        y = int(y * sV)
        w = int(w * sV)
        h = int(h * sV)

        shirtCenter = int((2 * x + w) / 2), min(y + 2 * h, im_cv.shape[0])

        shirtCorners = [(max(int(shirtCenter[0] - 2.5 * w), 0), max(y+h, 0)), (min(int(shirtCenter[0] + 2.5 * w), im_cv.shape[1]), min(shirtCenter[0] + 3 * h, im_cv.shape[0]))]

        #cv.rectangle(im_cv, (shirtCenter[0]-1, shirtCenter[1]-1), (shirtCenter[0]+1, shirtCenter[1]+1), (255, 255, 0), )
        cv.rectangle(im_cv, shirtCorners[0], shirtCorners[1], (255, 255, 0), 1)
    
        # im_cv = cv.cvtColor(im_cv, cv.COLOR_BGR2RGB)
        # im_pil = Image.fromarray(im_cv)

        # ImageDraw.floodfill(im_pil, shirtCenter, color, thresh=80)

        # im_np = np.asarray(im_pil)
        # im_cv = cv.cvtColor(im_np, cv.COLOR_RGB2BGR)

        
        k = cv.waitKey(30) & 0xff
        if k==27:
            run = False
            break

        im_cv_hsv = cv.cvtColor(im_cv, cv.COLOR_BGR2HSV)
        shirtColor = im_cv_hsv[shirtCenter[1] - 1][shirtCenter[0]]
        color = [0.3,0.7,1]
        shirtMask(im_cv, shirtColor, color, shirtCorners)

    cam.release()
    cv.destroyAllWindows()

def shirtMask(im_cv, maskColor, color, corners):

    # Convert to HSV
    hsv = cv.cvtColor(im_cv, cv.COLOR_BGR2HSV)

    

    # Define lower and upper limits of what we call "white-ish"
    sensitivity = 120
    lower = np.array([0, 0, 10])
    upper = np.array([255, 40, 245])

    # Create mask to only select white
    mask = cv.inRange(hsv, lower, upper)

    # Draw new rectangular mask on old mask that is black inside the rectangle and white outside the rectangle
    mask2 = mask.copy()
    cv.rectangle(mask2, corners[0], corners[1], 0, -1)

    # Change image to grey where we found white for combined mask
    #result = im_cv.copy()
    #result[mask2 > 0] = color

    a = np.where(mask > 0)
    ones = np.ones_like(im_cv)
    ones[a] = color
    result = im_cv*ones

    cv.imshow('mask2', mask2 )
    cv.imshow('bruh', im_cv)
    cv.imshow('mask', mask)

    result = cv.resize(result, (0, 0), fx=1, fy=1)
    cv.imshow('result', result)
    

if __name__ == "__main__":
    main()
