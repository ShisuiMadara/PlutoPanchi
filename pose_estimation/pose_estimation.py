import cv2
import pyrealsense2
from realsense_depth import *
import cv2.aruco as aruco
import zmq
import time

point = (400, 300)

# def show_distance(event, x, y, args, params):
#     global point
#     point = (x, y)

# Initialize Camera Intel Realsense
dc = DepthCamera()

# Create mouse event
# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame", show_distance)

publisher = None
def publish(data):

    stri = ""
    topic = "center"

    for i in data:
        stri += str(i)

    publisher.send_string(topic, flags=zmq.SNDMORE)
    publisher.send_string(stri)

def height(data):

    stri = str(data)

    topic = "height"

    print(stri)
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
    if draw:
        aruco.drawDetectedMarkers(img, bbox)

    return_dict = {}
    if bbox:

        x = (bbox[0][0][0][0] + bbox[0][0][2][0]) // 2
        x1 = (bbox[0][0][1][0] + bbox[0][0][3][0]) // 2
        
        y = (bbox[0][0][0][1] + bbox[0][0][2][1]) // 2
        y1 = (bbox[0][0][1][1] + bbox[0][0][3][1]) // 2

        center = ((x1 + x)// 2), int((y + y1)// 2)
        # print(center)
    
    publish(center)

    return center





if __name__ == '__main__':

    ctx = zmq.Context.instance()

    publisher = ctx.socket(zmq.XPUB)
    publisher.bind("tcp://127.0.0.1:6000")

    time.sleep(0.5)

    

    while True:
        ret, depth_frame, color_frame = dc.get_frame()

        center = detectMarker(color_frame)
        # Show distance for a specific point
        # print(point, center)

        if center:
            cv2.circle(color_frame, (int(center[0]), int(center[1])), 6, (0, 0, 255))
            distance = depth_frame[int(center[1]), int(center[0])]
            height(distance)
           
            cv2.putText(color_frame, "{}mm".format(distance), (point[0], point[1] - 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            detectMarker(color_frame)

        cv2.imshow("depth frame", depth_frame)
        cv2.imshow("Color frame", color_frame)
        key = cv2.waitKey(1)
        if key == 27:
            break

    ctx.term()
