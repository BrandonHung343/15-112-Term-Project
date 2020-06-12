import cv2
import numpy as np

window_name = "Webcam"
cam_index = 0
desired_size = 96.0

cv2.namedWindow(window_name)


face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_classifier = cv2.CascadeClassifier('haarcascade_eye.xml')

def reformat_for_processing(image):
    size = image.shape
    print(desired_size/size[0], desired_size/size[1])
    temp = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    s = cv2.resize(temp, (0,0), fx = desired_size/size[0], fy = desired_size/size[1])
    return s

def process(image, frame):
    size = frame.shape
    faces = face_classifier.detectMultiScale(image)
    eyes = eye_classifier.detectMultiScale(image)
    for face in faces:
        x1, y1, w, h = face
        cv2.rectangle(frame, (int(x1*size[0]/desired_size), int(y1*size[1]/desired_size)), (int((x1+w)*size[0]/desired_size), int((y1+h)*size[1]/desired_size)), (255, 255, 1), 5)
    
    for eye in eyes:
        x1, y1, w, h = eye
        cv2.rectangle(frame, (int(x1*size[0]/desired_size), int(y1*size[1]/desired_size)), (int((x1+w)*size[0]/desired_size), int((y1+h)*size[1]/desired_size)), (1, 255, 255), 5)
    return frame

def main():
    cap = cv2.VideoCapture(cam_index)
    while True:
        ref, frame = cap.read()

        if frame is not None:
            debug_frame = np.zeros(frame.shape, dtype=frame.dtype)
            formatted = reformat_for_processing(frame)
            final = process(formatted, frame)
        cv2.imshow(window_name, final)

        if cv2.waitKey(1) & 0xFF == 27:
            break


if __name__ == '__main__':
    main()