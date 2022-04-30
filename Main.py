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

        matches = RegionDetection.getMatchBounds(im_cv, 'upperBody')

        for (corner1, corner2) in matches:
            cv.rectangle(im_cv, corner1, corner2, (255, 0, 255), 2)

        im_cv = cv.cvtColor(im_cv, cv.COLOR_BGR2RGB)
        im_pil = Image.fromarray(im_cv)


        color = (255, 255, 255)

        shirtCenters = []
        for ((x, y), (a, b)) in matches:
            shirtCenters.append( ((a-x) * 2, b) )
        
        for coord in shirtCenters:
            ImageDraw.floodfill(im_pil, coord, color, thresh=50)

        im_np = np.asarray(im_pil)
        im_cv = cv.cvtColor(im_np, cv.COLOR_RGB2BGR)

        cv.imshow('bounding box gaming', im_cv)

        k = cv.waitKey(30) & 0xff
        if k==27:
            run = False
            break

    cam.release()

    

if __name__ == "__main__":
    main()
