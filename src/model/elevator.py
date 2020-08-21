import simpy
import queue

from .utils.utils import Direction, directionTowards, nextFloorTowards, directionToSymbol
from .registries.idle_registry import IdleRegistry
from .registries.scheduling_registry import SchedulingRegistry

class Elevator():
    """
    An elevator.
    An elevator is responsible for the states of its workers on queue and onboard.
    """
    def __init__(self, system, config):
        self.system = system

        self.scheduling = SchedulingRegistry.get(config.scheduling)
        self.idle = IdleRegistry.get(config.idle)
        self.capacity = config.capacity

        self.workersOnQueue = list()
        self.workersOnBoard = list()

        self.servingTime = 0
        self.waitingTime = 0

        self.currFloor = 1
        self.currDirection = Direction.none

        self.nextStop = 1

    def addWorkerOnQueue(self, worker):
        self.workersOnQueue.append(worker)
        worker.enterQueue()

    def update(self):
        self.currFloor = nextFloorTowards(fromFloor = self.currFloor, toFloor = self.nextStop)

        if (self.currFloor == self.nextStop):
            self.serveWorkersOnBoard(self.currFloor)
            self.serveWorkersOnQueue(self.currFloor)

        if (self.hasAnyWorkerToServe()):
            self.nextStop = self.scheduling.nextStop(self.system, self) # scheduling behaviour
            self.servingTime += 1
        else:
            self.nextStop = self.idle.idleFloor(self.system, self) # idle behaviour
            self.waitingTime += 1
        
        self.currDirection = directionTowards(fromFloor = self.currFloor, toFloor = self.nextStop)

    def hasAnyWorkerToServe(self): 
        return len(self.workersOnQueue) > 0 or len(self.workersOnBoard) > 0

    def isFull(self):
        return len(self.workersOnBoard) == self.capacity
    
    def goesInDirectionToFloor(self, floor):
        return directionTowards(fromFloor = self.currFloor, toFloor = floor) == self.currDirection

    def serveWorkersOnQueue(self, currFloor):
        for worker in self.workersOnQueue:
            if (worker.currFloor == currFloor and not self.isFull()):
                self.workersOnQueue.remove(worker)
                worker.leaveQueue()

                self.workersOnBoard.append(worker)
                worker.enterBoard(self)

    def serveWorkersOnBoard(self, currFloor):
        for worker in self.workersOnBoard:
            if (worker.destFloor == currFloor):
                self.workersOnBoard.remove(worker)
                worker.leaveBoard()
    
    def toString(self):

        return '|%d%s|[%s](%s)\n' % (
            self.currFloor, directionToSymbol(self.currDirection),
            ','.join(str(worker.destFloor) for worker in self.workersOnBoard),
            ','.join(str(worker.currFloor) for worker in self.workersOnQueue)
        )