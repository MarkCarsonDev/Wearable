import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
upperbody_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
lowerbody_cascade = cv2.CascadeClassifier('haarcascade_lowerbody.xml')

def getMatchBounds(image, region='body'):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if region == 'face':
        matches = face_cascade.detectMultiScale(
                                gray, 
                                scaleFactor=1.08, 
                                minNeighbors=3, 
                                minSize=(30, 30),
                                flags=cv2.CASCADE_SCALE_IMAGE)
    elif region == 'upperBody':
        matches = upperbody_cascade.detectMultiScale(
                                gray, 
                                scaleFactor=1.06, 
                                minNeighbors=4, 
                                minSize=(50, 50),
                                flags=cv2.CASCADE_SCALE_IMAGE)
    elif region == 'lowerBody':
        matches = lowerbody_cascade.detectMultiScale(
                                gray, 
                                scaleFactor=1.08, 
                                minNeighbors=3, 
                                minSize=(30, 30),
                                flags=cv2.CASCADE_SCALE_IMAGE)
    else:
        matches = body_cascade.detectMultiScale(
                                gray, 
                                scaleFactor=1.08, 
                                minNeighbors=3, 
                                minSize=(30, 30),
                                flags=cv2.CASCADE_SCALE_IMAGE)
   
    match = (0, 0, 1, 1)
    # Add the bounding box corners to upperBodyList as a tuple
    for (x, y, w, h) in matches:
        if (w * h) > match[2] * match[3]:
            match = (x, y, w, h)
    
    return match


