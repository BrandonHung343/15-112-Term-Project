# attempts at getting keypoints to do more complex image processing
# very interesting to learn about, but ultimately proved useless without 
# a sufficient dataset
import cv2
import numpy as np

def resize(image):
    size = image.shape
    target_size = 200.0
    return cv2.resize(image, (0,0), fx = target_size/size[0], fy = target_size/size[1])

def sifter(image, sift):
    kp = sift.detect(image, None)
    sifted = cv2.drawKeypoints(image, kp, image)
    return sifted

def main():
    h1 = cv2.imread('C:\\Users\Brandon\\source\\repos\\feature_detection_test\\feature_detection_test\\frame1.jpg', 0)
    sift = cv2.xfeatures2d.SIFT_create()
    cv2.namedWindow('H1')
    cv2.namedWindow('With Features Detected')
    h1 = resize(h1)
    cv2.namedWindow('With Threshold')
    cv2.imshow('H1', h1)
    features = sifter(h1, sift)
    cv2.imshow('With Features Detected', features)

    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

