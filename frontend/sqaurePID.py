import time
class PID:
    _Kp: list
    _Ki: list
    _Kd: list
    PID_Enabled : bool
    _prevTime : int
    _prevDistance : float
    targets: list
    _lowerBound: int
    _upperBound: int
    _bias: list
    _currentTargetIndex: int
    _threshold: float

    def __init__(
        self,
        targets: list,
        upper: int,
        lower: int,
        bias: list,
        proportionalConst: list,
        integralConst: list,
        deferentialConst: list,
        threshold: float
    ) -> None:
        self.PID_Enabled = True
        self.targets = targets
        self._Kp = proportionalConst
        self._Ki = integralConst
        self._Kd = deferentialConst
        self._lowerBound = lower
        self._upperBound = upper
        self._bias = bias
        self._threshold = threshold
        self._currentTargetIndex = 0

    def _getNextVal(self, currentDistance: float, idx: int) -> int:
        currentTime: int = self._getTime()
        label : str = 'Left-Right'
        if idx == 1:
            label = 'Forward-Back'
        elif idx == 2:
            label = 'Height'
        print(f'for {label}\n\r')
        print(f'Distance {currentDistance}\n\r')
        timeInterval: int = min(currentTime - self._prevTime, 25)
        print(f'Time Interval: {timeInterval}, {currentTime}, {self._prevTime}\n\r')
        currentError: float = self._getError(currentDistance, idx)
        D_Val: float = (self._Kd[idx] * currentError) / timeInterval
        P_Val: float = self._Kp[idx] * currentError
        I_Val: float = self._Ki[idx] * currentError * timeInterval
        PID_Val: int = round(self._bias[idx] + P_Val + I_Val + D_Val)
        print("Value is {} \n\r".format(PID_Val))
        print("Error is {} \n\r".format(currentError))
        print("PID Output is {} \n\r".format(PID_Val))
        # return output of PID
        return min(max(PID_Val, self._lowerBound), self._upperBound), currentError

    def startPIDController(
        self,
        dataFetcher,
        respondTo
    ) -> None:
        try:
            while 1:
                self._prevTime = self._getTime()
                time.sleep(0.001)
                if self.PID_Enabled:
                    dataFetcher()
                    recvData = dataFetcher().decode('utf-8').split()
                    print(f'{recvData}\n\r')

                    for i in range(len(recvData)):
                        if recvData[i] is None:
                            recvData[i] = 1500
                        if recvData[i] == 'None':
                            recvData[i] = 1500
                    print(recvData)
                    recievedData = [float(i)/1000 for i in recvData]
                    RPMS = []
                    Flag = True
                    if(self._currentTargetIndex < len(self.targets)):
                        for i in [0, 1, 2]:
                            newRPM, error = self._getNextVal(recievedData[i], i)
                            RPMS.append(newRPM)
                            if abs(error) > self._threshold:
                                Flag = False
                    if Flag and self._currentTargetIndex < len(self.targets):
                        self._currentTargetIndex += 1
                    elif Flag and self._currentTargetIndex == len(self.targets):
                        RPMS = [900, 900, 900]
                    print(f'{RPMS} {self._currentTargetIndex}\n\r')
                    respondTo(RPMS)
        except KeyboardInterrupt:
            pass
    def _getError(self, currentValue: float, idx: int) -> float:
        return -self.targets[self._currentTargetIndex][idx] + currentValue

    def _getTime(self) -> int:
        return round(time.time() * 1000)










