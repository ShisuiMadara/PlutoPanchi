import zmq

# from pid import PID
from squarePID import PID as sqPID
from multiprocessing import shared_memory
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
    # set parameters for PID controller
    targetHeight = 1.1
    targets = []  # left-right, front-back, height
    InitialThrottle = 1460
    InitialRoll = 1500
    InitialPitch = 1510
    acceptedErrorRange = 0.01
    # setup PID shared memory
    # this shared memory contains flag to enable and disable PID
    shm = shared_memory.SharedMemory(create=True, size=2)
    buffer = shm.buf
    buffer = bytearray([0, 0])
    # setup PID
    pidController: sqPID
    test = req(
        InitialRoll,
        InitialPitch,
        1500,
        InitialThrottle,
        True,
        True,
        False,
        False,
        0,
        publisher,
    )
    thread: Thread
    try:
        while key != ord("q"):
            key = stdscr.getch()
            if key == 49 and not buffer[0]:
                test.take_off()
                buffer = shm.buf
                buffer[0] = 1
                buffer[1] = 0
                if targets == []:
                    # if empty hover it at desired targetHeight
                    pidController = sqPID(
                        [[0, 0, targetHeight]],
                        2100,
                        900,
                        [InitialRoll, InitialPitch, InitialThrottle],
                        [3, 4.5, 0],
                        [0.0001, 0.1, 0],
                        [1.613, 0.6, 0],
                        -1,
                        shm.name,
                        test,
                    )
                else:
                    pidController = sqPID(
                        targets,
                        2100,
                        900,
                        [InitialRoll, InitialPitch, InitialThrottle],
                        [3, 4.5, 0],
                        [0.2, 0.1, 0],
                        [1.613, 0.6, 0],
                        # [4, 4, 0.9919],
                        # [15, 15, 0.09940],
                        # [35, 35, 0.047],
                        # [2, 2, 10],
                        # [1, 1, 0],
                        # [2, 2, 0],
                        acceptedErrorRange,
                        shm.name,
                        test,
                    )
                thread = Thread(
                    target=pidController.startPIDController,
                    args=(socket.recv, test.recieve_pid),
                )
                thread.start()
                print("Zooommm\n\r")
            elif key == 50:
                buffer[0] = 0
                buffer[1] = 0
                test.land()
                print("Landing safely....\n\r")
                thread.join()
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
            elif key == 115:
                test.backward()
                print("Going backward\n\r")
            elif key == 116 and not buffer[0]:
                print("Tracking drone now...\n\r")
                key = 0
                targets = []
                bu = 0
                while bu != ord("k"):
                    bu = stdscr.getch()
                    socket.recv()

                    recvData = socket.recv().decode("utf-8").split()
                    # print(recvData)
                    for i in range(len(recvData)):
                        if recvData[i] is None:
                            recvData[i] = 1500
                        if recvData[i] == "None":
                            recvData[i] = 1500
                    receivedData = [float(i) / 10 for i in recvData]
                    targets.append(receivedData)
                    print("Tracking\n\r")
            elif key == 97:
                test.left()
                print("Going left\n\r")
            elif key == 100:
                test.right()
                print("Going right\n\r")
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

            elif key == curses.KEY_DOWN:
                test.decrease_height()
                print("decreasing height...\n\r")
    except:
        print("Exception occured exiting...landing\n\r")
    # detach shared memory
    shm.close()
    shm.unlink()
    test.land()
    # disable raw mode
    curses.endwin()
    ctx.term()
