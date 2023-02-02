import time


class PID:
    _Kp: list
    _Ki: list
    _Kd: list
    PID_Enabled: bool
    _prevTime: int
    _prevDistance: float
    target: list
    _lowerBound: int
    _upperBound: int
    _bias: list

    def __init__(
        self,
        target: list,
        upper: int,
        lower: int,
        bias: list,
        proportionalConst: list,
        integralConst: list,
        deferentialConst: list,
    ) -> None:
        self.PID_Enabled = True
        self.target = target
        self._Kp = proportionalConst
        self._Ki = integralConst
        self._Kd = deferentialConst
        self._lowerBound = lower
        self._upperBound = upper
        self._bias = bias

    def _getNextVal(self, currentDistance: float, idx: int) -> int:
        currentTime: int = self._getTime()
        label: str = "Left-Right"
        if idx == 1:
            label = "Forward-Back"
        elif idx == 2:
            label = "Height"

        timeInterval: int = min(currentTime - self._prevTime, 25)
        currentError: float = self._getError(currentDistance, idx)
        D_Val: float = (self._Kd[idx] * currentError) / timeInterval
        P_Val: float = self._Kp[idx] * currentError
        I_Val: float = self._Ki[idx] * currentError * timeInterval
        PID_Val: int = round(self._bias[idx] + P_Val + I_Val + D_Val)
        return min(max(PID_Val, self._lowerBound), self._upperBound)

    def startPIDController(self, dataFetcher, respondTo) -> None:
        try:
            while 1:
                self._prevTime = self._getTime()
                time.sleep(0.001)
                if self.PID_Enabled:
                    dataFetcher()
                    recvData = dataFetcher().decode("utf-8").split()

                    for i in range(len(recvData)):
                        if recvData[i] is None:
                            recvData[i] = 1500
                        if recvData[i] == "None":
                            recvData[i] = 1500

                    recievedData = [float(i) / 1000 for i in recvData]
                    RPMS = []
                    for i in [0, 1, 2]:
                        RPMS.append(self._getNextVal(recievedData[i], i))
                    respondTo(RPMS)
        except KeyboardInterrupt:
            pass

    def _getError(self, currentValue: float, idx: int) -> float:
        return -self.target[idx] + currentValue

    def _getTime(self) -> int:
        return round(time.time() * 1000)
