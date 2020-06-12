import cv2

window_name = "Something"
#window_name = "Webcam!"
#cam_index = 0
#cv2.namedWindow(window_name)
#cap = cv2.VideoCapture(cam_index)
#cap.open(cam_index)

#inBlurMode = False
#while True:
#    ret, frame = cap.read()
#    if frame is not None:
#        if inBlurMode:
#            frame = cv2.blur(frame, (10,10))
#        cv2.imshow(window_name, frame)
#    k = cv2.waitKey(10) & 0xFF
#    if k == 27:
#        cap.destroyAllWindows()
#        cap.release()
#        breal
#    if k == ord('b'):
#        inBlurMode = not inBlurMode

image = cv2.imread('test2.jpg')

desired_size = 500.0

if image is not None:
    size = image.shape
    blurred = cv2.blur(image, (100,100), 5)
    resizeIm = cv2.resize(blurred, (0,0), fx = desired_size/size[0], fy = desired_size/size[1]/2)
    cv2.imshow(window_name, resizeIm)
    cv2.waitKey(0)
    
if image is not None:
    window_name = "Image 2"
    imRe = cv2.resize(image, (0,0), fx = desired_size/size[0], fy = desired_size/size[1]/2)
    cv2.imshow(window_name, imRe)
    cv2.waitKey(0)

cv2.destroyAllWindows()

