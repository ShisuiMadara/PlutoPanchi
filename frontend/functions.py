import zmq
from zmq.devices import monitored_queue

ctx = zmq.Context.instance()
publisher = ctx.socket(zmq.PUB)
publisher.bind("tcp://*:6000")


def publish(data):
    stri = ""

    for i in range(0, data.length()):
        stri += data

        if(i == data.length - 1):
            continue

        stri += ","

        try:
            publisher.send(stri.encode('utf-8'))
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                throw(e.errno)
            else:
                raise
        time.sleep(0.1)


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

        self.publish(arr)

    def disarm(self):

        # do disarming
        self.is_armed = False

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def forward(self):

        self.pitch += 200

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]

        self.publish(arr)

    def backward(self):

        self.pitch -= 200

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]

        self.publish(arr)

    def left(self):

        self.roll -= 200

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def right(self):

        self.roll += 200

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def left_yaw(self):

        self.yaw -= 200

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def right_yaw(self):

        self.yaw += 200

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def increase_height(self):

        self.throttle += 100

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def decrease_height(self):

        self.throttle -= 100

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def take_off(self):

        self.arm()
        self.command_type = 1

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def land(self):

        self.command_type = 2

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def back_flip(self):

        self.command_type = 3

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def front_flip(self):

        self.command_type = 4

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def right_flip(self):

        self.command_type = 5

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def left_flip(self):

        self.command_type = 6

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def set_roll(self, rol):

        self.roll = rol
        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def set_pitch(self, pit):

        self.pitch = pit

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)  # publish

    def set_yaw(self, ya):

        self.yaw = ya
        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def set_throttle(self, throt):

        self.throttle = throt

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)

    def reset(self):

        self.roll = 1500
        self.yaw = 1500
        self.pitch = 1500
        self.throttle = 1500

        arr = [str(self.roll), str(self.pitch), str(self.yaw), str(self.throttle), str(
            self.head_free), str(self.dev_mode), str(self.alt_hold), str(self.is_armed)]
        self.publish(arr)


if __name__ == '__main__':
    test = req()
