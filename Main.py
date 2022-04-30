# Libraries
import cv2 as cv

# Local classes
import Webcam
import FindFaces as faces

def main():
    cam = cv.VideoCapture(0)
    image = Webcam.get_image(cam, mirror=True)

    faces.facebox()

if __name__ == "__main__":
    main()
