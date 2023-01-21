import sys 
sys.path.append("../")
import zmq 
import time
import curses
from frontend.functions import *


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