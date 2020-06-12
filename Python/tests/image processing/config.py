import cv2

# Used to dynamically configure frame filters with a gui
# Deprecated by the voice controlled calibration

def makeTrackBars(windowName):
    cv2.createTrackbar('H_Lower', windowName, lower_red[0], (low_red[0]+lower_red[0])//2, nothing)
    cv2.createTrackbar('S_Lower', windowName, lower_red[1], (low_red[1]+lower_red[1])//2, nothing)
    cv2.createTrackbar('V_Lower', windowName, lower_red[2], (low_red[2]+lower_red[2])//2, nothing)
    cv2.createTrackbar('H_Low', windowName, (low_red[0]+lower_red[0])//2, low_red[0], nothing)
    cv2.createTrackbar('S_Low', windowName, (low_red[1]+lower_red[1])//2, low_red[1], nothing)
    cv2.createTrackbar('V_Low', windowName, (low_red[2]+lower_red[2])//2, low_red[2], nothing)

    cv2.createTrackbar('H_High', windowName, high_red[0], (high_red[0]+higher_red[0])//2, nothing)
    cv2.createTrackbar('S_High', windowName, high_red[1], (high_red[1]+higher_red[1])//2, nothing)
    cv2.createTrackbar('V_High', windowName, high_red[2], (high_red[2]+higher_red[2])//2, nothing)
    cv2.createTrackbar('H_Higher', windowName, (high_red[0]+higher_red[0])//2, higher_red[0], nothing)
    cv2.createTrackbar('S_Higher', windowName, (high_red[1]+higher_red[1])//2, higher_red[1], nothing)
    cv2.createTrackbar('V_Higher', windowName, (high_red[2]+higher_red[2])//2, higher_red[2], nothing)
    

def getTrackBars(windowName):
    lower_red[0] = cv2.getTrackbarPos('H_Lower', windowName)
    lower_red[1] = cv2.getTrackbarPos('S_Lower', windowName)
    lower_red[2] = cv2.getTrackbarPos('V_Lower', windowName)
    low_red[0] = cv2.getTrackbarPos('H_Low', windowName)
    low_red[1] = cv2.getTrackbarPos('S_Low', windowName)
    low_red[2] = cv2.getTrackbarPos('V_Low', windowName)

    high_red[0] = cv2.getTrackbarPos('H_High', windowName)
    high_red[1] = cv2.getTrackbarPos('S_High', windowName)
    high_red[2] = cv2.getTrackbarPos('V_High', windowName)
    higher_red[0] = cv2.getTrackbarPos('H_Higher', windowName)
    higher_red[1] = cv2.getTrackbarPos('S_Higher', windowName)
    higher_red[2] = cv2.getTrackbarPos('V_Higher', windowName)
