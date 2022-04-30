import cv2


def get_image(camera, mirror=False):
        img = camera.read()
        if mirror: 
            img = cv2.flip(img, 1)
        return img

if __name__ == '__main__':
    main()