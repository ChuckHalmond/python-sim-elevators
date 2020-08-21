from abc import ABCMeta, abstractmethod
from src.model.elevator import Elevator
from src.model.utils.utils import Direction, directionTowards

class SchedulingBase(metaclass = ABCMeta):

    @abstractmethod
    def nextStop(self, system, elevator):
        pass

class SchedulingFCFS(SchedulingBase):

    def nextStop(self, system, elevator):
        nbWorkersOnBoard = len(elevator.workersOnBoard)
        nbWorkersOnQueue = len(elevator.workersOnQueue)

        if (nbWorkersOnBoard > 0):
            return elevator.workersOnBoard[0].destFloor
        elif (nbWorkersOnQueue > 0):
            return elevator.workersOnQueue[0].currFloor
        else:
            return 1

class SchedulingSSTF(SchedulingBase):

    def nextStop(self, system, elevator):
        closestDestFloor = None
        closestDestFloorDistance = system.config.floors

        for worker in elevator.workersOnBoard:
            destFloor = worker.destFloor
            destFloorDistance = abs(elevator.currFloor - destFloor)
            if (destFloorDistance <= closestDestFloorDistance):
                closestDestFloor = destFloor
                closestDestFloorDistance = destFloorDistance

        if (not elevator.isFull()):
            for worker in elevator.workersOnQueue:
                destFloor = worker.currFloor
                destFloorDistance = abs(elevator.currFloor - destFloor)
                if (destFloorDistance <= closestDestFloorDistance):
                    closestDestFloor = destFloor
                    closestDestFloorDistance = destFloorDistance

        if (closestDestFloor == None):
            return elevator.currFloor

        return closestDestFloor

class SchedulingLS(SchedulingBase):

    def nextStop(self, system, elevator):
        closestDestFloor = None
        closestDestFloorDistance = system.config.floors

        for worker in elevator.workersOnBoard:
            # checks that the worker & the elevator seek to go in the same direction
            if (elevator.currDirection == Direction.none or
                directionTowards(fromFloor = elevator.currFloor, toFloor = worker.destFloor) == elevator.currDirection):
                # SSTF strategy
                destFloor = worker.destFloor
                destFloorDistance = abs(elevator.currFloor - destFloor)
                if (destFloorDistance <= closestDestFloorDistance):
                    closestDestFloor = destFloor
                    closestDestFloorDistance = destFloorDistance

        if (not elevator.isFull()):
            for worker in elevator.workersOnQueue:
                # checks that the worker & the elevator seek to go in the same direction
                if (elevator.currDirection == Direction.none or 
                    directionTowards(fromFloor = elevator.currFloor, toFloor = worker.destFloor) == elevator.currDirection):
                    # SSTF strategy
                    destFloor = worker.currFloor
                    destFloorDistance = abs(elevator.currFloor - destFloor)
                    if (destFloorDistance <= closestDestFloorDistance):
                        closestDestFloor = destFloor
                        closestDestFloorDistance = destFloorDistance

        if (closestDestFloor == None):
            return elevator.currFloor

        return closestDestFloor