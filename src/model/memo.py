class Memo():

    def __init__(self):
        self.waitingTimeDone = 0
        self.servingTimeDone = 0
        self.workingTimeDone = 0
        self.workersDone = 0

    def memorizeWorkerData(self, worker):
        self.waitingTimeDone += worker.waitingTime
        self.servingTimeDone += worker.servingTime
        self.workingTimeDone += worker.workingTime
        self.workersDone += 1