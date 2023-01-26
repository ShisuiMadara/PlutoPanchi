import cv2
import pyrealsense2
from realsense_depth import *
import cv2.aruco as aruco
import zmq
import time
import math

point = (400, 300)


# Initialize Camera Intel Realsense
dc = DepthCamera()

publisher = None
def publish(data):

    stri = ""
    topic = "center"

    for i in data:
        stri += str(i)

    publisher.send_string(topic, flags=zmq.SNDMORE)
    publisher.send_string(stri)

def height(data):

    print(data)
    stri = ""

    topic = "height"

    for i in range (0,len(data)):
        
        if(data[i] == ',' or data[i] == '[' or data[i] == ']'):
            continue

        stri += str(data[i]) 

        if(i == len(data)-1):
            continue
        stri += " "
        #distance from LR, distance from FB, height


    # print(stri)
    publisher.send_string(topic, flags=zmq.SNDMORE)
    publisher.send_string(stri)


def detectMarker(img, markerSize=4, totalMarker=50, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarker}')
    arucoDict = aruco.getPredefinedDictionary(key)

    arucoParam = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(arucoDict, arucoParam)
    bbox, ids, rejected = detector.detectMarkers(imgGray,)
    center = ()

    (h, w) = color_frame.shape[:2]
    # print(h,w)
    cv2.circle(color_frame, (w//2, h//2), 7, (255, 255, 255), -1) 

    distance_from_center_LR = None
    distance_from_center_FB = None
    head_back_to = [None, None]

    if draw:
        aruco.drawDetectedMarkers(img, bbox)

    return_dict = {}
    if bbox:

        x = (bbox[0][0][0][0] + bbox[0][0][2][0]) / 2
        x1 = (bbox[0][0][1][0] + bbox[0][0][3][0]) / 2
        
        y = (bbox[0][0][0][1] + bbox[0][0][2][1]) / 2
        y1 = (bbox[0][0][1][1] + bbox[0][0][3][1]) / 2


        # print(x,x1,y,y1)

        center = ((x1 + x)// 2), int((y + y1)// 2)
        # print("-----bbox---------")
        # print(center)
        # print(aruco_center)
        # print("-----------------")

        distance_from_center_LR = abs(center[0]- w/2) 
        distance_from_center_FB = abs(center[1]- h/2)

        # print("---------------")
        # print(distance_from_center_FB)
        # print(distance_from_center_LR)
        # print("---------------")

        if (center[0] < w/2):
            head_back_to[0] = 'R'
            
        else:
            head_back_to[0] = 'L'
            distance_from_center_LR = -distance_from_center_LR

        if (center[1] < h/2):
            head_back_to[1] = 'B'
            distance_from_center_FB = -distance_from_center_FB
        else:
            head_back_to[1] = 'F'    
        
        # print("-----------------")
        # print(head_back_to)
        # print("------------------")
        # print("-----------center------------")
        # print(center)
        # print("---------aaaaaaaaaaaaaaa------------")
            
        # print(distance_from_center)
        # print(head_back_to)
        # print(center, w//2, h//2)
    
        publish(center)

    arr = [center, distance_from_center_LR, distance_from_center_FB]
    # print(arr)

    return arr





if __name__ == '__main__':

    ctx = zmq.Context.instance()

    publisher = ctx.socket(zmq.XPUB)
    publisher.bind("tcp://127.0.0.1:6001")

    time.sleep(0.5)

    

    while True:
        ret, depth_frame, color_frame = dc.get_frame()

     

        center = detectMarker(color_frame)[0]
        # print(center)
        # Show distance for a specific point
        # print(point, center)

        if center:
            # print("here")
            # print(center)
            cv2.circle(color_frame, (int(center[0]), int(center[1])), 6, (0, 0, 255))
            distance = depth_frame[int(center[1]), int(center[0])]

            cv2.putText(color_frame, "{}mm".format(distance), (point[0], point[1] - 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            arr = detectMarker(color_frame)

            if(arr[1] == None or arr[2] == None):
                pass 
            else:
                arr.append(distance)
                arr.pop(0)

                print(arr)
                height(arr)
                tup = center

            # print("UPDATED TUPLE")
            # print(tup)
            # print("------------------")

        
        cv2.imshow("depth frame", depth_frame)
        cv2.imshow("Color frame", color_frame)
        key = cv2.waitKey(1)
        if key == 27:
            break

    ctx.term()
