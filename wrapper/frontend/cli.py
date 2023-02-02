import zmq


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
        publisher,
    ):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        self.throttle = throttle
        self.head_free = head_free
        self.dev_mode = dev_mode
        self.alt_hold = alt_hold
        self.is_armed = is_armed
        self.publisher = publisher

    def publish(self, data):
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

        self.publisher.send_string(topic, flags=zmq.SNDMORE)
        self.publisher.send_string(stri)

    def cmd_publisher(self, cmd_type):
        stri = ""

        topic = "cmd"
        stri += str(cmd_type)

        self.publisher.send_string(topic, flags=zmq.SNDMORE)
        self.publisher.send_string(stri)

    def listener_thread(pipe):
        while True:
            try:
                print(f"{pipe.recv_multipart()}\n\r")
            except zmq.ZMQError as e:
                if e.errno == zmq.ETERM:
                    break

    def arm(self):
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

        self.publish(arr)
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

        self.publish(arr)

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

        self.publish(arr)
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

        self.publish(arr)
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

        self.publish(arr)
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
        self.publish(arr)
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
        self.publish(arr)

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
        self.publish(arr)

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
        self.publish(arr)

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
        self.publish(arr)

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
        self.publish(arr)

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
       
        self.publish(arr)
        self.cmd_publisher(self.command_type)

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
        self.publish(arr)
        self.cmd_publisher(self.command_type)

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
        self.publish(arr)
        self.cmd_publisher(self.command_type)

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
        self.publish(arr)
        self.cmd_publisher(self.command_type)

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
        self.publish(arr)
        self.cmd_publisher(self.command_type)

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
        self.publish(arr)
        self.cmd_publisher(self.command_type)

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
        self.publish(arr)

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
        self.publish(arr)  # publish

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
        self.publish(arr)

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
        self.publish(arr)

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
        self.publish(arr)

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

        self.publish(arr)
