# Libraries
import cv2 as cv

# Local classes
import Webcam

def main():
    cam = cv.VideoCapture(0)
    img = Webcam.get_image(cam, mirror=True)

if __name__ == "__main__":
    main()