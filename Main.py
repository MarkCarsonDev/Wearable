# Libraries
import cv2 as cv
import numpy as np


# Local classes
import Webcam
import RegionDetection


def main():
    # Start a camera using CV
    cam = cv.VideoCapture(0)
    color = [0.4, 0.6, 0.4]

    while (True):
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

        shirtCorners = [(max(int(shirtCenter[0] - 2.5 * w), 0), max(y+h, 0)), (min(int(
            shirtCenter[0] + 2.5 * w), im_cv.shape[1]), min(shirtCenter[0] + 3 * h, im_cv.shape[0]))]

        cv.rectangle(im_cv, shirtCorners[0], shirtCorners[1], (255, 255, 0), 1)

        k = cv.waitKey(30) & 0xff
        if k == 27:
            # ESC exits the program
            break
        if k == 49:
            color = [0, 0, 0]
        if k == 50:
            color = [0.3, 0.3, 0.3]
        if k == 51:
            color = [0.6, 0.6, 0.6]
        if k == 52:
            color = [1, 1, 1]
        if k == 53:
            color = [color[0] - 0.1, color[1], color[2]]
        if k == 54:
            color = [color[0] + 0.1, color[1], color[2]]
        if k == 55:
            color = [color[0], color[1] - 0.1, color[2]]
        if k == 56:
            color = [color[0], color[1] + 0.1, color[2]]
        if k == 57:
            color = [color[0], color[1], color[2] - 0.1]
        if k == 58:
            color = [color[0], color[1], color[2] + 0.1]
        if color[0] > 1 or color[0] < 1:
            color[0] = 0.1
        if color[1] > 1 or color[1] < 1:
            color[1] = 0.1
        if color[2] > 1 or color[2] < 1:
            color[2] = 0.1

        im_cv_hsv = cv.cvtColor(im_cv, cv.COLOR_BGR2HSV)
        shirtColor = im_cv_hsv[shirtCenter[1] - 1][shirtCenter[0]]

        shirtMask(im_cv, shirtColor, color, shirtCorners)

    cam.release()
    cv.destroyAllWindows()


def shirtMask(im_cv, maskColor, color, corners):

    # Convert to HSV
    hsv = cv.cvtColor(im_cv, cv.COLOR_BGR2HSV)

    # Color options
    sensitivity = 120
    lower = np.array([0, 0, 20])
    upper = np.array([255, 60, 245])

    # Create mask to only select white
    mask = cv.inRange(hsv, lower, upper)

    # Draw new rectangular mask for the shirt region
    mask2 = mask.copy()
    cv.rectangle(mask2, corners[0], corners[1], 0, -1)

    # Overlay masks and multiply
    a = np.where(mask > 0)
    ones = np.ones_like(im_cv)
    color = [round(color[0], 2), round(color[1], 2), round(color[2], 2)]
    ones[a] = color
    result = im_cv*ones

    cv.imshow('mask2', mask2)
    cv.imshow('bruh', im_cv)
    cv.imshow('mask', mask)

    result = cv.resize(result, (0, 0), fx=1, fy=1)
    cv.imshow('result', result)
    print(color)


if __name__ == "__main__":
    main()
