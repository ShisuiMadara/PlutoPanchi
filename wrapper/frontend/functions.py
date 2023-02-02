import zmq
from pid import PID
from sqaurePID import PID as sqPID
from zmq.devices import monitored_queue
from threading import Thread
import time
import curses
from cli import *

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
    test = req(InitialRoll, InitialPitch, 1500, InitialThrottle, True, True, False, False, 0, publisher)
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

