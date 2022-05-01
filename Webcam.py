import numpy as np
import cv2

def get_image(camera, mirror=False):
        ret_val, img = camera.read()
        if mirror: 
            img = cv2.flip(img, 1)
        return img
