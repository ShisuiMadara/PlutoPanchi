import time
from multiprocessing import shared_memory
from array import array
from cli import req


class PID:
    _Kp: list
    _Ki: list
    _Kd: list
    _prevTime: int
    _prevDistance: float
    targets: list
    _lowerBound: int
    _upperBound: int
    _bias: list
    _currentTargetIndex: int
    _threshold: float
    _sharedMemoryName: str
    _droneController: req

    def __init__(
        self,
        targets: list,
        upper: int,
        lower: int,
        bias: list,
        proportionalConst: list,
        integralConst: list,
        deferentialConst: list,
        threshold: float,
        shm_Name: str,
        droneController: req,
    ) -> None:
        self.targets = targets
        self._Kp = proportionalConst
        self._Ki = integralConst
        self._Kd = deferentialConst
        self._lowerBound = lower
        self._upperBound = upper
        self._bias = bias
        self._threshold = threshold
        self._currentTargetIndex = 0
        self._sharedMemoryName = shm_Name
        self._droneController = droneController

    def _getNextVal(self, currentDistance: float, idx: int) -> int:
        currentTime: int = self._getTime()
        timeInterval: int = max(min(currentTime - self._prevTime, 25), 1)
        currentError: float = self._getError(currentDistance, idx)
        D_Val: float = (self._Kd[idx] * currentError) / timeInterval
        P_Val: float = self._Kp[idx] * currentError
        I_Val: float = self._Ki[idx] * currentError * timeInterval
        PID_Val: int = round(self._bias[idx] + P_Val + I_Val + D_Val)
        if self._Kp[idx] == 0 and self._Ki[idx] == 0 and self._Kd[idx] == 0:
            currentError = 0
        # if self._Kp[idx] == 0.9919 and self._Ki[idx] == 0.09940 and self._Kd[idx] == 0.047:
        #     currentError = 0
        return min(max(PID_Val, self._lowerBound), self._upperBound), currentError

        #  [2, 2, 0.9919],
        #                 [1, 1, 0.09940],
        #                 [2, 2, 0.047],

    def startPIDController(self, dataFetcher, respondTo) -> None:
        shm = shared_memory.SharedMemory(self._sharedMemoryName)
        try:
            buffer = shm.buf
            while buffer[0]:
                # print(buffer[0])
                self._prevTime = self._getTime()
                # time.sleep(0.001)
                dataFetcher()
                recvData = dataFetcher().decode("utf-8").split()
                for i in range(len(recvData)):
                    if recvData[i] is None:
                        recvData[i] = 1500
                    if recvData[i] == "None":
                        recvData[i] = 1500

                recievedData = [float(i) / 10 for i in recvData]

                # print(recievedData)
                RPMS = []
                Flag = True
                print(self._currentTargetIndex, end="\n\r")
                print(len(self.targets), end="\n\r")
                if self._currentTargetIndex < len(self.targets):
                    for i in [0, 1, 2]:
                        newRPM, error = self._getNextVal(recievedData[i], i)
                        RPMS.append(newRPM)
                        print(error, end=" ")
                        if abs(error) > self._threshold:
                            Flag = False
                print(f"\n\r{Flag}", end="\n\r")
                if Flag and self._currentTargetIndex < len(self.targets):
                    self._currentTargetIndex += 1
                    RPMS = self._bias
                    respondTo(RPMS)
                    time.sleep(1)
                elif Flag and self._currentTargetIndex == len(self.targets):
                    buffer[1] = 1
                    print("Tracing completed... now landing\n\r")
                    self._droneController.land()
                    break
                respondTo(RPMS)
        except KeyboardInterrupt:
            pass
        shm.close()

    def _getError(self, currentValue: float, idx: int) -> float:
        return currentValue - float(self.targets[self._currentTargetIndex][idx])

    def _getTime(self) -> int:
        return round(time.time() * 1000)
