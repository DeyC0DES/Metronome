class BeatsCalc:
    def __init__(self):
        super().__init__()

    def calcBps(self, bpm):
        try:
            return bpm / 60
        except ZeroDivisionError:
            return

    def calcSleepTime(self, bps):
        try:
            return 1 / bps
        except ZeroDivisionError:
            return