import time
import zmq 

class PID:
    _Kp: int
    _Ki: int
    _Kd: int
    _prevTime : int
    _prevDistance : float
    _target: float
    _lowerBound: int
    _upperBound: int
    _bias: int

    def __init__(
        self,
        target: float,
        upper: int,
        lower: int,
        bias: int,
        proportionalConst: int = 0,
        integralConst: int = 0,
        deferentialConst: int = 0,
    ) -> None:
        self._Kp = proportionalConst
        self._Ki = integralConst
        self._Kd = deferentialConst
        self._target = target
        self._lowerBound = lower
        self._upperBound = upper
        self._bias = bias

    def _getNextVal(self, currentDistance: float) -> int:
        currentTime: int = self._getTime()
        print(f'Distance {currentDistance}')
        timeInterval: int = currentTime - self._prevTime
        currentError: float = self._getError(currentDistance)
        D_Val: float = (self._Kd * currentError) / timeInterval
        P_Val: float = self._Kp * currentError
        I_Val: float = self._Ki * currentError * timeInterval
        PID_Val: int = round(self._bias + P_Val + I_Val + D_Val)
        print("Value is {}".format(PID_Val))
        print("Error is {}".format(currentError))
        # update prevDistance and prevTime
        self._prevTime = currentTime
        # return output of PID
        return min(max(PID_Val, self._lowerBound), self._upperBound)

    def startPIDController(
        self,
        dataFetcher,
        respondTo
    ) -> None:
        PID_Enabled : bool = True

        self._prevTime = self._getTime()
        while 1:
            if PID_Enabled:
                dataFetcher()
                nextRPM : int = self._getNextVal(float(dataFetcher().decode('utf-8'))/1000)
                respondTo(nextRPM)

    def _getError(self, currentValue: float) -> float:
        return self._target - currentValue

    def _getTime(self) -> int:
        return round(time.time() * 1000)


def fun (s) :
    pass


if __name__ == '__main__':

    host = "127.0.0.1"
    port = "6000"
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://{}:{}".format(host, port))
    socket.subscribe("height")
    expected_height = 1.5
    pid = PID (expected_height, 2100, 900, 1500, 200, 0, 50)

    # print(current_height)

    pid.startPIDController(socket.recv, print )



    
