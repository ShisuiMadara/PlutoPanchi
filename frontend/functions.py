import zmq
from zmq.devices import monitored_queue
from threading import Thread
import time 

publisher = None
def publish(data):
    stri = ""

    topic = "front"

    for i in range(0, len(data)):
        stri += str(data[i])

        if(i == len(data) - 1):
            continue

        stri += ","
    

    publisher.send_string(topic)
    publisher.send_string(stri)

def cmd_publisher(cmd_type):

    stri = ""

    topic = "cmd"
    stri += str(cmd_type)

    print(stri)
    publisher.send_string(topic)
    publisher.send_string(stri)
   


def listener_thread (pipe):
    
    while True:
        try:
            print (pipe.recv_multipart())
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break           


class req ():

    def __init__(self, roll, pitch, yaw, throttle, head_free, dev_mode, alt_hold, is_armed, command_type):

        self.roll = 1500
        self.pitch = 1500
        self.yaw = 1500
        self.throttle = 1500
        self.head_free = True
        self.dev_mode = True
        self.alt_hold = True
        self.is_armed = False

    def arm(self):

        # do arming
        self.is_armed = True

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]

        publish(arr)

    def disarm(self):

        # do disarming
        self.is_armed = False

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        
        publish(arr)

    def forward(self):

        self.pitch += 200

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]

        publish(arr)

    def backward(self):

        self.pitch -= 200

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]

        publish(arr)

    def left(self):

        self.roll -= 200

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def right(self):

        self.roll += 200

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def left_yaw(self):

        self.yaw -= 200

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def right_yaw(self):

        self.yaw += 200

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def increase_height(self):

        self.throttle += 100

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def decrease_height(self):

        self.throttle -= 100

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def take_off(self):

        self.arm()
        self.command_type = 1

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def land(self):

        self.command_type = 2

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def back_flip(self):

        self.command_type = 3

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def front_flip(self):

        self.command_type = 4

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def right_flip(self):

        self.command_type = 5

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def left_flip(self):

        self.command_type = 6

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def set_roll(self, rol):

        self.roll = rol
        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def set_pitch(self, pit):

        self.pitch = pit

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)  # publish

    def set_yaw(self, ya):

        self.yaw = ya
        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def set_throttle(self, throt):

        self.throttle = throt

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def reset(self):

        self.roll = 1500
        self.yaw = 1500
        self.pitch = 1500
        self.throttle = 1500

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)


if __name__ == '__main__':

    ctx = zmq.Context.instance()

    test = req(1500,1500,1500,1500,True,True,True,False,0)

    data = [1500,1500,1500,1500,True,True,True,False]

    cmd_type = 0

    publisher = ctx.socket(zmq.XPUB)
    publisher.bind("tcp://127.0.0.1:6000")

    time.sleep(0.5)

    publish(data)

    cmd_publisher(cmd_type)

    # p_thread = Thread(target=publish(data))
    # p_thread.start()

    # del  publisher
    ctx.term()

