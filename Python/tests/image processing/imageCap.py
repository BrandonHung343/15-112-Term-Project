# Used to capture positive images for haar classifier
import cv2
import numpy as np


def main():
    count = 0
    cap = cv2.VideoCapture(0)
    cap.open(0)
    # meant to set frame rate, didn't work
    # cap.set(cv2.CAP_PROP_FPS, 10) 
    cv2.namedWindow('Something')
    
    while True:
        ret, frame = cap.read()
        if frame is not None:
            
            cv2.imshow('Something', frame)
        
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()
            cap.release()
            break
        # takes 3 images when a is pressed, labels and saves them
        elif k == ord('a'):
            for c in range(1, 4):
                cv2.imwrite('frame%d.jpg' % (count+1), frame)
                print('Captured %d' % (count+1))
                count += 1
        

if __name__ == '__main__':
    main()