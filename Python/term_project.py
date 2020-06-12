from __future__ import division
import math
import cv2
import speech_recognition as sr  
import threading
import pyaudio
import numpy as np
import socket
import sys
import decimal
import time

# filter arrays
low_blue = np.array([70, 80, 120])
high_blue = np.array([140, 255, 255])
click_set_low = np.zeros((1,3))
click_set_high = np.zeros((1,3))

# instantiates socket
TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024

s = socket.socket()
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
connection, address = s.accept()

current_word = None
refresh = 0

# creates threadLock object
threadLock = threading.Lock()
seppuku = False

word_bank = ['stay', 'free', '1', '2', '3', 'track', 'grab', 'calibrate']

# creates tag and item location variables
tag_center = (0,0)
item_center = (0,0)
tag_ref = 0
points_per_mm = 3.32
tag_size = 50.8
z = 304.8 

last_point = (0, 0, 0)

tag_area = 0
item_area = 0
item_x = 0
item_y = 0
tag_x = 0
tag_y = 0
depth = 0
item_depth = None
frames = 0
mode = 0

scale = 5.3
delta = 60
depth_scale = 0

set_flag = False
mask_set = False

demo_hsv = None

desired_size = 100.0

# computes euclidean distances between points
def euclidean(last, point):
    x, y, z = point
    x0, y0, z0 = last
    return (math.sqrt((x0-x)**2 + (y0-y)**2 + (z0-z)**2))
    
# From 112 Website
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

# wrapper to extract data from frames
def process(frame, connection, window, draw, window_name):
    global click_set_low, click_set_high, mask_set
    if mask_set:
        colored, cnt = color_threshold(frame, click_set_low, click_set_high, mask_set)
        cv2.imshow(draw, colored)
    item, _ = color_threshold(frame)
    check_dist()
    follow_hand(frame, connection)
    cv2.imshow(window, frame)
    cv2.imshow(window_name, item)

# dummy required to run get_or_set
def nothing(tbDummy):
    pass

# gets the hsv value at the x y coordinate you click on
def get_or_set(event, x, y, flags, param):
    global mask_set, tag_ref, tag_area
    if event == cv2.EVENT_LBUTTONDOWN:
        print demo_hsv[y,x]
    elif event == cv2.EVENT_RBUTTONDOWN:
        set(x,y)

# sets color filters
def set(x, y):
    global click_set_low, click_set_high, tag_ref, tag_area, mask_set, set_flag
    for i in range(3):
        if i == 0:
            if demo_hsv[y,x][i] < delta:
                click_set_low[0][i] = 0
            else:
                click_set_low[0][i] =  demo_hsv[y,x][i] - delta
            if demo_hsv[y,x][i] + delta > 180:
                click_set_high[0][i] = 180
            else:
                click_set_high[0][i] =  demo_hsv[y,x][i] + delta
        else:
            if demo_hsv[y,x][i] + delta > 255:
                click_set_high[0][i] = 255
            else:
                click_set_high[0][i] = demo_hsv[y,x][i] + delta
            if demo_hsv[y,x][i] - delta < 0:
                click_set_low[0][i] = 0
            else:
                click_set_low[0][i] = demo_hsv[y,x][i] - delta
    mask_set = True
    set_flag = True
    
def color_threshold(image, lower=low_blue, higher=high_blue, mask_yes = False, set=False):
    global delta
    global tag_center, tag_size, tag_area
    global item_area, item_center, item_x, item_y
    global points_per_mm
    
    size = image.shape
    thresheld = np.zeros(size)
    # smoothes edges
    image = cv2.bilateralFilter(image, 9, 75, 75)
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # filters image
    mask = cv2.inRange(frame, lower, higher)
    _, cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    maxSize = 0
    maxCnt = None
    for cnt in cnts:
        if cnt.size > maxSize:
            maxSize = cnt.size
            maxCnt = cnt
        mask = cv2.drawContours(mask, [cnt], -1, [255], -1)
    # computes biggest contour and uses it to calculate distances
    if maxCnt is not None:
        x,y,w,h = cv2.boundingRect(maxCnt)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),5)
        if mask_yes:
            # computes reference tag angles
            x,y,w,h = cv2.boundingRect(maxCnt)
            tag_center = ((2*x+w)//2, (2*y+h)//2)
            tag_area = w*h
            points_per_mm = w/tag_size
        else:
            item_area = w*h
            item_center = ((x+w)//2, (y+h)//2)
    thresheld = cv2.bitwise_and(image, image, mask = mask) # applies mask to image
    return thresheld, maxCnt
    
def check_dist():
    # computes item's distance relative to tag's
    global item_center, item_area, item_depth, item_x, item_y
    global delta, z, points_per_mm, scale, depth
    global tag_center, tag_area, tag_ref
    
    if item_center != (0,0) and tag_center != (0,0):
        s = item_area/tag_area
        print(s)
        if tag_ref != 0 and tag_area > 10:
            depth = math.sqrt(tag_ref/tag_area)*z
            x1, y1 = tag_center
            item_depth = roundHalfUp(math.sqrt(s**-1)*depth) * scale
            x, y = item_center
            depth_scale = item_depth/depth
            item_x = roundHalfUp(x/(points_per_mm/depth_scale))
            item_y = roundHalfUp(y/(points_per_mm/depth_scale))

# processes speech inputs
def voice_recorder(m, r, connection):
    global mode, seppuku, word_bank, current_word, refresh
    global threadLock, click_set_low, click_set_high, demo_hsv
    
    with m as source:
        while True:
            if seppuku:
                break
            print('Speak:')
            # records 2 second clips
            audio = r.record(source, 2)
            
            try:
                word = r.recognize_google(audio)
                print(word)
                word = word.strip()
                threadLock.acquire()
                refresh = time.time()
                
                if word in word_bank:
                    if word == 'calibrate':
                        size = demo_hsv.shape
                        x = size[0]
                        y = size[1]
                        set(x//2, y//2)
                    else:
                        current_word = word
                        connection.send((word + '~').encode('utf-8'))
                        if current_word == 'track':
                            mode = 1
                        elif current_word == 'grab':
                            mode = 2
                        else:
                            mode = 0
                threadLock.release()
                
            except sr.UnknownValueError:
                if current_word != None and time.time() - refresh > 0.5 and \
                current_word != 'track':
                    connection.send((current_word+'~').encode('utf-8'))
                pass
                
            except sr.RequestError as e:
                print("Google Speech Recognition service dieded".format(e))
                
def follow_hand(image, connection):
    global tag_center, depth, points_per_mm, z, frames, threadLock, mode, item_center
    
    size = image.shape
    # link lengths of the arm
    x_scale, y_scale, z_scale = 0.2, 0.3, 0.5
    depth_scale = depth/z
    x, y = tag_center
    max_depth = 635
    
    if depth_scale != 0:
        # normalizes point coordinates
        point = ((x-(size[1]//2))/(size[1]//2//depth_scale),
        (y-(size[0]//2))/(size[0]//2//depth_scale),
        depth/max_depth)
        
        if frames % 7 == 0 and mode == 1:
            x1, y1, z1 = point
            # Normalizes arm's coordinates relative to camera frame
            xs ='%0.3f' % (z1*z_scale) 
            ys = '%0.3f' % (x1*x_scale*-1)
            zs = '%0.3f' % (y1*y_scale*-1)
            point_str = str(xs)+'_'+str(ys)+'_'+str(zs)+'~'
            # Transmits point to socket
            threadLock.acquire()
            connection.send(point_str.encode('utf-8'))
            threadLock.release()
            print point_str
        # computes defined non-tag object coordinates and sends coordinates
        elif frames % 7 == 0 and mode == 2 and item_center != None:
            obj_x, obj_y = item_center
            obj_point = ((obj_x-(size[1]//2))/(size[1]//2//depth_scale),
            (obj_y-(size[0]//2))/(size[0]//2//depth_scale), 
            item_depth/max_depth)
            obj_x, obj_y, obj_z = obj_point
            obj_xs ='%0.3f' % (obj_z*z_scale)
            obj_ys = '%0.3f' % (obj_x*x_scale*-1)
            obj_zs = '%0.3f' % (obj_y*scale*-1)
            obj_point_str = str(obj_xs)+'_'+str(obj_ys)+'_'+str(obj_zs)+'~'
            threadLock.acquire()
            connection.send(obj_point_str.encode('utf-8'))
            threadLock.release()
            print obj_point_str
        last_point = point
    frames += 1

# spins up voice_recognition thread
def voice_recognition():
    global connection, t
    r = sr.Recognizer()
    r.energy_threshold = 1000 #arbitrary, did not want to adjust for ambient noise each time
    m = sr.Microphone()
    m.SAMPLE_RATE = 48000
    
    t = threading.Thread(target=voice_recorder, args=(m, r, connection))
    t.start()
    
def main():
    global demo_hsv, item_center, item_depth, word, connection, seppuku
    global click_set_low, click_set_high, tag_ref, tag_area, set_flag
    
    sys.stdout.write("It has begun \n")
    sys.stdout.flush()
    
    # creates windows and streams
    cam = 0
    window = "Tech Demo"
    cv2.namedWindow(window)
    cv2.setMouseCallback(window, get_or_set)
    draw = "Draw"
    cv2.namedWindow(draw)
    cap = cv2.VideoCapture(cam)
    cap.open(cam)
    window_name = 'item'
    cv2.namedWindow(window_name)
    
    voice_recognition()
    
    while True:
        try:
            ret, frame = cap.read()
            if frame is not None:
                demo_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                process(frame, connection, window, draw, window_name)
            if set_flag:
                tag_ref = tag_area
            set_flag = False
            # ESC to exit and close
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                print(k)
                seppuku = True
                cv2.destroyAllWindows()
                cap.release()
                s.close()
                break
                
        except:
            print('Died')
            seppuku = True
            cv2.destroyAllWindows()
            cap.release()
            s.close()
            break

   
if __name__ == '__main__':
    main()