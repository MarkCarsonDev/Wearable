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

        matches = RegionDetection.getMatchBounds(im_cv, 'face')

        for (corner1, corner2) in matches:
            cv.rectangle(im_cv, corner1, corner2, (255, 0, 255), 2)

        sV = 0.2

        im_cv = cv.cvtColor(im_cv, cv.COLOR_BGR2RGB)
        im_cv = cv.resize(im_cv, (0, 0), fx=sV, fy=sV)

        im_pil = Image.fromarray(im_cv)


        color = (255, 255, 255)


        shirtCenters = []
        for ((x, y), (a, b)) in matches:
            x = int(x * sV)
            y = int(y * sV)
            a = int(a * sV)
            b = int(b * sV)
            
            shirtCenters.append( ((a-x) * 2, b) )
            if (b - y) > 3 and (a - x) > 3: 
                print(f"{x},{y} to {a},{b}")
                cv.imshow('bounding box gaming', im_cv[y:b, x:a])
    
        
        for coord in shirtCenters:
            ImageDraw.floodfill(im_pil, coord, color, thresh=65)

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
