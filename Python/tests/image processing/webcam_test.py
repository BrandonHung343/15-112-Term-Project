import cv2

window_name = "Webcam!"

cam_index = 0

cv2.namedWindow(window_name)

cap = cv2.VideoCapture(cam_index)
cap.open(cam_index)

while True:

    ret, frame = cap.read()

    if frame is not None:
        cv2.imshow(window_name, frame)

        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            cv2.destroyAllWindows()
            cap.release()
            break
