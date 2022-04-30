# Libraries
import cv2 as cv
from PIL import Image, ImageDraw

# Local classes
import Webcam
import RegionDetection 

def main():
    cam = cv.VideoCapture(0)
    run = True

    while (run):
        image = Webcam.get_image(cam, mirror=True)

        matches = RegionDetection.getMatchBounds(image, 'upperBody')

        for (corner1, corner2) in matches:
            cv.rectangle(image, corner1, corner2, (255, 0, 255), 2)

        matches = RegionDetection.getMatchBounds(image, 'lowerBody')

        for (corner1, corner2) in matches:
            cv.rectangle(image, corner1, corner2, (0, 0, 255), 2)

        matches = RegionDetection.getMatchBounds(image, 'face')

        for (corner1, corner2) in matches:
            cv.rectangle(image, corner1, corner2, (255, 255, 255), 2)

        cv.imshow('bounding box gaming', image)

        k = cv.waitKey(30) & 0xff
        if k==27:
            run = False
            break

    cam.release()

    

if __name__ == "__main__":
    main()
