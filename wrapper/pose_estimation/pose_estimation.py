import cv2
import pyrealsense2
from realsense_depth import *
import cv2.aruco as aruco
import zmq
import time
import math

point = (400, 300)


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

    for i in range(0, len(data)):
        if data[i] == "," or data[i] == "[" or data[i] == "]":
            continue

        stri += str(data[i])

        if i == len(data) - 1:
            continue
        stri += " "

    publisher.send_string(topic, flags=zmq.SNDMORE)
    publisher.send_string(stri)


def detectMarker(img, markerSize=4, totalMarker=50, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f"DICT_{markerSize}X{markerSize}_{totalMarker}")
    arucoDict = aruco.getPredefinedDictionary(key)

    arucoParam = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(arucoDict, arucoParam)
    bbox, ids, rejected = detector.detectMarkers(
        imgGray,
    )
    center = ()

    (h, w) = color_frame.shape[:2]

    cv2.circle(color_frame, (w // 2, h // 2), 7, (255, 255, 255), -1)

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

        center = ((x1 + x) // 2), int((y + y1) // 2)

        distance_from_center_LR = abs(center[0] - w / 2)
        distance_from_center_FB = abs(center[1] - h / 2)

        if center[0] < w / 2:
            head_back_to[0] = "R"

        else:
            head_back_to[0] = "L"
            distance_from_center_LR = -distance_from_center_LR

        if center[1] < h / 2:
            head_back_to[1] = "B"
            distance_from_center_FB = -distance_from_center_FB
        else:
            head_back_to[1] = "F"

        publish(center)

    arr = [center, distance_from_center_LR, distance_from_center_FB]

    return arr


if __name__ == "__main__":
    ctx = zmq.Context.instance()

    publisher = ctx.socket(zmq.XPUB)
    publisher.bind("tcp://127.0.0.1:6001")

    time.sleep(0.5)

    while True:
        time.sleep(0.01)
        ret, depth_frame, color_frame = dc.get_frame()
        center = detectMarker(color_frame)

        if center[0]:
            cv2.circle(
                color_frame, (int(center[0][0]), int(center[0][1])), 6, (0, 0, 255)
            )
            distance = depth_frame[int(center[0][1]), int(center[0][0])]

            cv2.putText(
                color_frame,
                "{}mm".format(distance),
                (point[0], point[1] - 200),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                (0, 0, 255),
                2,
            )
            arr = center

            if arr[1] == None or arr[2] == None:
                pass
            else:
                arr.append(distance)
                arr.pop(0)

                height(arr)
                tup = center

        cv2.imshow("depth frame", depth_frame)
        cv2.imshow("Color frame", color_frame)
        key = cv2.waitKey(1)
        if key == 27:
            break

    ctx.term()
