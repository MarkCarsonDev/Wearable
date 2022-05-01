from tkinter import *
import numpy as np
import cv2
from PIL import Image, ImageTk

def get_image(camera, mirror=False):
        ret_val, img = camera.read()
        if mirror: 
            img = cv2.flip(img, 1)
        return img

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    while (True):


        img = get_image(cam, mirror=True)

        #Create an instance of tkinter frame
        win = Tk()
        win.geometry("700x550")
        #Load the image
        #img = cv2.imread('tutorialspoint.png')

        #Rearrange colors
        blue,green,red = cv2.split(img)
        img = cv2.merge((red,green,blue))
        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im)

        #Create a Label to display the image
        Label(win, image= imgtk).pack()
        win.mainloop()


        if cv2.waitKey(1) == 27: 
            break  # esc to quit
        cv2.destroyAllWindows()