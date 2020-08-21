class Worker():
    """
    A worker.
    The state of the worker should only be updated from external events, i.e its methods.
    """
    def __init__(self, destFloor, worktime): 
        self.currFloor = 1
        self.destFloor = destFloor
        self.worktime = worktime
        self.elevator = None
        
        self.waitingTime = 0
        self.servingTime = 0
        self.workingTime = 0

        self.isOnQueue = False
        self.isOnBoard = False

        self.isAtWork = False
        self.hasWorked = False
        self.isDone = False

        self.isOnQueueRequest = True

    def enterQueue(self):
        self.isOnQueueRequest = False
        self.isOnQueue = True

    def leaveQueue(self):
        self.isOnQueue = False

    def enterBoard(self, elevator):
        self.elevator = elevator
        self.isOnBoard = True

    def leaveBoard(self):
        self.isOnBoard = False
        self.elevator = None

        if (not self.hasWorked):
            self.enterWorkplace()
        else:
            self.isDone = True

    def enterWorkplace(self):
        self.isAtWork = True

    def leaveWorkplace(self):
        self.isAtWork = False
        self.hasWorked = True
        self.destFloor = 1

        self.isOnQueueRequest = True

    def update(self):

        if (self.isOnBoard):
            self.currFloor = self.elevator.currFloor
            self.servingTime += 1

        elif (self.isAtWork):
            self.workingTime += 1
            if (self.workingTime >= self.worktime):
                self.leaveWorkplace()
        else:
            self.waitingTime += 1

    
    