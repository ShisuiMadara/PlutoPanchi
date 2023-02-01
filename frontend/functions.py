import zmq
from pid import PID
from sqaurePID import PID as sqPID
from zmq.devices import monitored_queue
from threading import Thread
import time
import curses

publisher = None


def publish(data):
    stri = ""

    topic = "front"

    for i in range(0, len(data)):

        if data[i] == True:
            data[i] = 1
        elif data[i] == False:
            data[i] = 0

        stri += str(data[i])

        if i == len(data) - 1:
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


def listener_thread(pipe):

    while True:
        try:
            print(f"{pipe.recv_multipart()}\n\r")
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break


class req:
    def __init__(
        self,
        roll,
        pitch,
        yaw,
        throttle,
        head_free,
        dev_mode,
        alt_hold,
        is_armed,
        command_type,
    ):

        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        self.throttle = throttle
        self.head_free = head_free
        self.dev_mode = dev_mode
        self.alt_hold = alt_hold
        self.is_armed = is_armed

    def arm(self):

        # do arming
        self.is_armed = True

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]

        publish(arr)
        print("ARM IS CALLED\n\r")

    def disarm(self):

        # do disarming
        self.is_armed = False

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]

        publish(arr)

    def forward(self):

        self.pitch = min(self.pitch + 100, 2100)

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]

        publish(arr)
        print("FORWARD IS CALLED\n\r")

    def resend(self):

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]

        publish(arr)
        print("FORWARD IS CALLED\n\r")

    def backward(self):
        print("initial pitch {}\n\r".format(self.pitch))

        self.pitch = max(self.pitch - 100, 900)

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]

        publish(arr)
        print("BACKWARD IS CALLED\n\r")

    def left(self):

        self.roll = max(self.roll - 100, 900)

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)
        print("LEFT IS CALLED\n\r")

    def right(self):

        self.roll = min(self.roll + 100, 2100)

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)

        print("RIGHT IS CALLED\n\r")

    def left_yaw(self):

        if self.yaw == 900:
            print("Max left yaw reached\n\r")
            pass

        self.yaw = max(self.yaw - 100, 900)

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)

    def right_yaw(self):

        if self.yaw == 2100:
            print("Max right yaw reached\n\r")

        self.yaw = min(self.yaw + 100, 2100)

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)

    def increase_height(self):

        if self.throttle == 2100:
            print("Max throttle. Cannot increase\n\r")
            pass

        self.throttle = min(self.throttle + 100, 2100)

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)

    def decrease_height(self):

        if self.throttle == 900:
            print("Throttle at minimum. Cannot decrease\n\r")
            pass

        self.throttle = max(self.throttle - 100, 900)

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)

    def take_off(self):

        if not self.is_armed:
            self.arm()
        self.command_type = 1

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        print(f'{arr}\n\r')
        publish(arr)
        cmd_publisher(self.command_type)

    def land(self):

        self.command_type = 2

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)
        cmd_publisher(self.command_type)

    def back_flip(self):

        self.command_type = 3

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)
        cmd_publisher(self.command_type)

    def front_flip(self):

        self.command_type = 4

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)
        cmd_publisher(self.command_type)

    def right_flip(self):

        self.command_type = 5

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)
        cmd_publisher(self.command_type)

    def left_flip(self):

        self.command_type = 6

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)
        cmd_publisher(self.command_type)

    def set_roll(self, rol):

        self.roll = rol
        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)

    def set_pitch(self, pit):

        self.pitch = pit

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)  # publish

    def set_yaw(self, ya):

        self.yaw = ya
        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)

    def set_throttle(self, throt):

        self.throttle = throt

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)

    def reset(self):

        self.roll = 1500
        self.yaw = 1500
        self.pitch = 1500
        self.throttle = 1500

        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        publish(arr)

    def recieve_pid(self, pid_output):
        self.roll = pid_output[0]
        self.pitch = pid_output[1]
        self.throttle = pid_output[2]
        arr = [
            str(self.roll),
            str(self.pitch),
            str(self.throttle),
            str(self.yaw),
            str(self.head_free),
            str(self.dev_mode),
            str(self.alt_hold),
            str(self.is_armed),
        ]
        print(f'Publish data: {arr}\n\r')
        publish(arr)

    def mok(self):
        print("hoi\n\r")


if __name__ == "__main__":
    ctx = zmq.Context.instance()
    publisher = ctx.socket(zmq.XPUB)
    publisher.bind("tcp://127.0.0.1:6000")
    time.sleep(0.5)
    stdscr = curses.initscr()
    stdscr.keypad(1)
    stdscr.addstr("Hit 'q' to quit\n\r")
    stdscr.refresh()
    key = ""
    # setup PID
    host = "127.0.0.1"
    port = "6001"
    socket = zmq.Context().socket(zmq.SUB)
    socket.connect(f"tcp://{host}:{port}")
    socket.subscribe("height")
    currentTarget = 0
    targetHeight = 1.4
    targets = [[0, 0, targetHeight], [-0.177, -0.141, targetHeight], [0.167, -0.136, targetHeight], [0.156, 0.099, targetHeight], [-0.095, 0.093, targetHeight], [-0.177, -0.141, targetHeight]]   # left-right, front-back, height
    InitialThrottle = 1460
    InitialRoll = 1483
    InitialPitch = 1501
    # pidController = PID (targets[0], 2100, 900, [InitialRoll, InitialPitch, InitialThrottle], [300, 300, 500], [10, 10, 20], [15, 15, 10])
    pidController = sqPID (targets, 2100, 900, [InitialRoll, InitialPitch, InitialThrottle], [2, 2, 0], [1, 1, 0], [2, 2, 0], 0.07)
    # pidController = PID (targets, 2100, 900, [InitialRoll, InitialPitch, InitialThrottle], [0, 0, 0], [0, 0, 0], [0, 0, 0])
    test = req(InitialRoll, InitialPitch, 1500, InitialThrottle, True, True, False, False, 0)
    Thread(target=pidController.startPIDController, args = (socket.recv, test.recieve_pid)).start()
    # Thread(target=pidController.startPIDController, args = (socket.recv, )).start()
    # Thread(target = test.mok()).start()
    while key != ord("q"):
        key = stdscr.getch()
        print(key)
        if key == 49:
            test.take_off()
            print("Zooommm\n\r")
        elif key == 50:
            test.land()
            print("Landing safely....\n\r")
            # Thread(target = test.recieve_pid()).start()
        elif key == 51:
            test.back_flip()
            print("Back FLIP !!!\n\r")
        elif key == 52:
            test.front_flip()
            print("Front FLIPP !!!!\n\r")
        elif key == 53:
            test.right_flip()
            print("Right FLIP!!!\n\r")
        elif key == 54:
            test.left_flip
            print("LEFT FLIPP!!\n\r")
        elif key == 119:
            test.forward()
            print("Going forward...\n\r")
            # test.recieve_pid()
        elif key == 115:
            test.backward()
            print("Going backward\n\r")
            # test.recieve_pid()
        elif key == 97:
            test.left()
            print("Going left\n\r")
            # test.recieve_pid()
        elif key == 100:
            test.right()
            print("Going right\n\r")
            # test.recieve_pid()
        elif key == 32:
            if test.is_armed:
                test.land()
                print("Landing safely to disarm\n\r")
                test.disarm()
                print("Disarmed\n\r")
            else:
                test.arm()
                print("Arming !!\n\r")
        elif key == curses.KEY_UP:
            test.increase_height()
            print("increasing height...\n\r")
            # Thread(target = test.recieve_pid()).start()
        elif key == curses.KEY_DOWN:
            test.decrease_height()
            print("decreasing height...\n\r")
            # Thread(target = test.recieve_pid()).start()
        # else:
        # Thread(target = test.recieve_pid()).start()

    curses.endwin()
    # publish(data)
    # cmd_publisher(cmd_type)

    # p_thread = Thread(target=publish(data))
    # p_thread.start()

    # del  publisher
    ctx.term()
