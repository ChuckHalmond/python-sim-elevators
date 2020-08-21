from abc import ABCMeta, abstractmethod
from src.model.utils.utils import Direction

class IdleBase(metaclass = ABCMeta):

    @abstractmethod
    def idleFloor(self, system, elevator):
        pass

class IdleBottom(IdleBase):

    def idleFloor(self, system, elevator):
        return 1

class IdleMiddle(IdleBase):

    def idleFloor(self, system, elevator):
        return system.config.floors / 2

class IdleOnPlace(IdleBase):

    def idleFloor(self, system, elevator):
        return elevator.currFloor

class IdleYoyo(IdleBase):

    def idleFloor(self, system, elevator):
        if (elevator.currDirection != Direction.up and elevator.currFloor > 1):
            return 1
        elif (elevator.currDirection != Direction.down and elevator.currFloor < system.config.floors):
            return system.config.floors
        else:
            return system.config.floors / 2
            
