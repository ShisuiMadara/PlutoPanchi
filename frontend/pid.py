import time
import zmq
from threading import Thread

class PID:
    _Kp: list
    _Ki: list
    _Kd: list
    PID_Enabled : bool
    _prevTime : int
    _prevDistance : float
    target: list
    _lowerBound: int
    _upperBound: int
    _bias: int

    def __init__(
        self,
        target: list,
        upper: int,
        lower: int,
        bias: int,
        proportionalConst: list,
        integralConst: list,
        deferentialConst: list,
    ) -> None:
        self.PID_Enabled = True
        self._Kp = proportionalConst
        self._Ki = integralConst
        self._Kd = deferentialConst
        self.target = target
        self._lowerBound = lower
        self._upperBound = upper
        self._bias = bias

    def _getNextVal(self, currentDistance: float, idx: int) -> int:
        currentTime: int = self._getTime()
        label : str = 'Left-Right'
        if idx == 1:
            label = 'Forward-Back'
        elif idx == 2:
            label = 'Height'
        print(f'for {label}')
        print(f'Distance {currentDistance}')
        timeInterval: int = currentTime - self._prevTime
        print(f'Time Interval: {timeInterval}, {currentTime}, {self._prevTime}')
        currentError: float = self._getError(currentDistance, idx)
        D_Val: float = (self._Kd[idx] * currentError) / timeInterval
        P_Val: float = self._Kp[idx] * currentError
        I_Val: float = self._Ki[idx] * currentError * timeInterval
        PID_Val: int = round(self._bias + P_Val + I_Val + D_Val)
        print("Value is {}".format(PID_Val))
        print("Error is {}".format(currentError))
        print("PID Output is {}".format(PID_Val))
        # return output of PID
        return min(max(PID_Val, self._lowerBound), self._upperBound)

    def startPIDController(
        self,
        dataFetcher,
        respondTo
    ) -> None:
        self._prevTime = self._getTime()
        while 1:
            time.sleep(0.001)
            if self.PID_Enabled:
                dataFetcher()
                recvData = dataFetcher().decode('utf-8').split()

                for i in range(len(recvData)):
                    if recvData[i] is None:
                        recvData[i] = 1500
                    if recvData[i] == 'None':
                        recvData[i] = 1500

                recievedData = [float(i)/1000 for i in recvData]
                print(recievedData)
                RPMS = []
                for i in [0, 1, 2]:
                    RPMS.append(self._getNextVal(recievedData[i], i))
                self._prevTime = self._getTime()
                respondTo(RPMS)

    def _getError(self, currentValue: float, idx: int) -> float:
        return -self._target[idx] + currentValue

    def _getTime(self) -> int:
        return round(time.time() * 1000)











