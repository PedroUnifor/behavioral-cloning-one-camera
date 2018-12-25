import numpy as np
import cv2

ip = 'http://187.25.88.127:8080/video'
cap = cv2.VideoCapture(ip)

while(True):

    ret, frame = cap.read()
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
