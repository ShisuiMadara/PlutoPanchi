import time
from pynput.keyboard import Listener

class PID:
    _Kp: int
    _Ki: int
    _Kd: int
    _prevTime : int
    _prevDistance : float
    _target: float
    _lowerBound: int
    _upperBound: int

    def __init__(
        self,
        target: float,
        upper: int,
        lower: int,
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

    def _getNextVal(self, currentDistance: float) -> int:
        currentTime: int = self._getTime()
        timeInterval: int = currentTime - self._prevTime
        currentError: float = self._getError(currentDistance, self._prevDistance)
        D_Val: float = (self._Kd * currentError) / timeInterval
        P_Val: float = self._Kp * currentError
        I_Val: float = self._ki * currentError * timeInterval
        PID_Val: int = round(P_Val + I_Val + D_Val)
        # update prevDistance and prevTime
        self._prevDistance = currentDistance
        self._prevTime = currentTime
        # return output of PID
        return min(max(PID_Val, self._lowerBound), self._upper)

    def startPIDController(
        self,
        dataFetcher : function,
        respondTo : function
    ) -> None:
        PID_Enabled : bool = True
        # add listener to break as any key is pressed
        def toggle():
            PID_Enabled = not PID_Enabled
        with Listener(on_press = toggle) as listener:
            listener.join()
        # initialize PID controller with current Value and current time
        self._prevTime = self._getTime
        self._prevDistance : float = float(dataFetcher())
        while 1:
            if PID_Enabled:
                nextRPM : int = self._getNextVal(dataFetcher())
                respondTo(nextRPM)

    def _getError(self, previousValue: float, currentValue: float) -> float:
        return currentValue - previousValue

    def _getTime(self) -> int:
        return round(time.time() * 1000)
