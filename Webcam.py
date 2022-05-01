import cv2
import eel 

#@eel.expose
def get_image(camera, mirror=False):
        ret_val, img = camera.read()
        if mirror: 
            img = cv2.flip(img, 1)
        return img

if __name__ == '__main__':
    #eel.init("website")

    #eel.start("camera.html")
    cam = cv2.VideoCapture(0)
    while (True):
        cv2.imshow('FitYoShit', get_image(cam, mirror=True))
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
        cv2.destroyAllWindows()