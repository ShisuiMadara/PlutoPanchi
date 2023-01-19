import zmq
from zmq.devices import monitored_queue
from threading import Thread
import time 
import curses

publisher = None
def publish(data):
    stri = ""

    topic = "front"

    for i in range(0, len(data)):

        if(data[i] == True):
            data[i] = 1
        elif (data[i] == False):
            data[i] = 0

        stri += str(data[i])

        if(i == len(data) - 1):
            continue

        stri += " "
    

    publisher.send_string(topic, flags=zmq.SNDMORE)
    publisher.send_string(stri)

def cmd_publisher(cmd_type):

    stri = ""

    topic = "cmd"
    stri += str(cmd_type)

    publisher.send_string(topic, flags=zmq.SNDMORE)
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

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]

        publish(arr)
        print("ARM IS CALLED ")

    def disarm(self):

        # do disarming
        self.is_armed = False

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        
        publish(arr)

    def forward(self):

        self.pitch = min(self.pitch + 100, 2100)
        
        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]

        
        publish(arr)
        print("FORWARD IS CALLED ")
    
    def resend (self):

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]

        
        publish(arr)
        print("FORWARD IS CALLED ")


    def backward(self):
        print("initial pitch {}".format(self.pitch))

        self.pitch = max(self.pitch - 100, 900)

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]

        
        publish(arr)
        print("BACKWARD IS CALLED")

    def left(self):

        self.roll = max(self.roll - 100, 900)

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)
        print("LEFT IS CALLED")

    def right(self):

        self.roll = min(self.roll + 100, 2100)

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

        print("RIGHT IS CALLED")

    def left_yaw(self):

        if(self.yaw == 900):
            print("Max left yaw reached")
            pass

        self.yaw = max(self.yaw - 100, 900)

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def right_yaw(self):

        if(self.yaw == 2100):
            print("Max right yaw reached")

        self.yaw = min(self.yaw + 100, 2100) 

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def increase_height(self):

        if(self.throttle == 2100):
            print("Max throttle. Cannot increase")
            pass

        self.throttle = min(self.throttle + 100, 2100)

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def decrease_height(self):

        if(self.throttle == 900):
            print("Throttle at minimum. Cannot decrease")
            pass 

        self.throttle = max(self.throttle - 100, 900)

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def take_off(self):

        if(not self.is_armed):
            self.arm()
        self.command_type = 1

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)
        cmd_publisher(self.command_type)

    def land(self):

        self.command_type = 2

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)
        cmd_publisher(self.command_type)

    def back_flip(self):

        self.command_type = 3

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)
        cmd_publisher(self.command_type)

    def front_flip(self):

        self.command_type = 4

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)
        cmd_publisher(self.command_type)

    def right_flip(self):

        self.command_type = 5

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)
        cmd_publisher(self.command_type)

    def left_flip(self):

        self.command_type = 6

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)
        cmd_publisher(self.command_type)

    def set_roll(self, rol):

        self.roll = rol
        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def set_pitch(self, pit):

        self.pitch = pit

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)  # publish

    def set_yaw(self, ya):

        self.yaw = ya
        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def set_throttle(self, throt):

        self.throttle = throt

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)

    def reset(self):

        self.roll = 1500
        self.yaw = 1500
        self.pitch = 1500
        self.throttle = 1500

        arr = [str(self.roll), str(self.pitch), str(self.throttle), str(self.yaw), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        publish(arr)


if __name__ == '__main__':

    ctx = zmq.Context.instance()

    # data = [1500,1500,1500,1500,True,True,True,False]

    # cmd_type = 0

    publisher = ctx.socket(zmq.XPUB)
    publisher.bind("tcp://127.0.0.1:6000")

    time.sleep(0.5)

    stdscr = curses.initscr()

    stdscr.keypad(1)

    stdscr.addstr("Hit 'q' to quit")
    stdscr.refresh()

    key = ''
    test = req(1500,1500,1500,1500,True,True,True,False,0)

    while key != ord('q'):
        key = stdscr.getch()
        
    
        if key == 49: 
            test.take_off()
            print("Zooommm")
        elif key == 50: 
            test.land()
            print("Landing safely....")
        elif key == 51:
            test.back_flip()
            print("Back FLIP !!!")
        elif key == 52:
            test.front_flip()
            print("Front FLIPP !!!!")
        elif key == 53:
            test.right_flip()
            print("Right FLIP!!!")
        elif key == 54:
            test.left_flip
            print("LEFT FLIPP!!")
        

        elif key == 119:
            test.forward()
            print("Going forward...")
        elif key == 115:
            test.backward()
            print("Going backward")
        elif key == 97:
            test.left()
            print("Going left")
        elif key == 100:
            test.right()
            print("Going right")
        elif key == 32:

            if(test.is_armed):
                test.land()
                print("Landing safely to disarm")
                test.disarm()
                print("Disarmed")   
            else:
                test.arm()
                print("Arming !!")

        elif key == curses.KEY_UP:
            test.increase_height()
            print("increasing height...")
        elif key == curses.KEY_DOWN:
            test.decrease_height()
            print("decreasing height...")
    
        

    curses.endwin()


    # publish(data)
    # cmd_publisher(cmd_type)

    # p_thread = Thread(target=publish(data))
    # p_thread.start()

    # del  publisher
    ctx.term()