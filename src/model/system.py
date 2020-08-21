from .rand.rng import RandomNumberGenerator
from .worker import Worker
from .elevator import Elevator
from .memo import Memo
from .config import Config
from .utils.io import line

import time

class System():
    """
    The System of the simulation.
    The System is responsible for the coordination between the arrivals of new workers and the elevators.
    """
    def __init__(self, env, config: Config):
        self.env = env
        self.config = config

        self.workers = list()
        self.elevators = list()

        self.rng = RandomNumberGenerator(config.randSeed)
        self.memo = Memo()

    def start(self):
        # instantiates the elevators
        for _ in range(self.config.elevators):
            self.elevators.append(Elevator(self, self.config))
        
        # launches the mainLoop
        self.env.process(self.mainLoop())
        self.env.run()


    def mainLoop(self):

        while (self.env.now < self.config.steps):
    
            # tests if a new worker arrives
            aNewWorkerArrives = self.rng.poisson(self.config.mu) == 1
            if (aNewWorkerArrives):
                self.generateNewWorker(self.config.lbda, self.config.floors)

            # updates the workers state
            for worker in self.workers:

                # if the worker is on queue request
                # tries to add him on an elevator queue
                if (worker.isOnQueueRequest):
                    self.tryAddWorkerOnQueue(worker)

                # memorizes the worker data and removes it from the list
                # whenever he is done
                if (worker.isDone):
                    self.onWorkerDone(worker)
            
                worker.update()

            # updates the elevators state
            for elevator in self.elevators:
                elevator.update()

            # if live mode is enabled, displays some live information
            if (self.config.live):
                self.displayLive()
                time.sleep(self.config.liveDelay)

            yield self.env.timeout(1)
        
        # memorizes the remaining workers data
        for worker in self.workers:
            self.onWorkerDone(worker)

        # recaps the simulation
        if (self.config.recap):
            self.displayConfigRecap()
            self.displayWorkersRecap()
            self.displayElevatorsRecap()

    def generateNewWorker(self, lbda, floors):
        destFloor = self.rng.randint(2, floors)
        worktime = self.rng.exponential(lbda)
        worker = Worker(destFloor, worktime)
        self.workers.append(worker)

    def tryAddWorkerOnQueue(self, worker):
        for elevator in self.elevators:
            if (elevator.goesInDirectionToFloor(worker.currFloor)):
                elevator.addWorkerOnQueue(worker)
                return
        for elevator in self.elevators:
            if (not elevator.hasAnyWorkerToServe()):
                elevator.addWorkerOnQueue(worker)
                return
    
    def onWorkerDone(self, worker):
        self.memo.memorizeWorkerData(worker)
        self.workers.remove(worker)

    def displayLive(self):
        workersOnQueueRequestStr = ''

        for worker in self.workers:
            if (worker.isOnQueueRequest):
                workersOnQueueRequestStr += str(worker.currFloor) + ','

        workersOnQueueRequestStr = workersOnQueueRequestStr.rstrip(',')

        print('{s=%s}(%s)' % (str(self.env.now), workersOnQueueRequestStr))
        for elevator in self.elevators:
            print(elevator.toString(), end = '')
        print()
    
    def displayConfigRecap(self):
        print(line)
        print('Config Recap')
        print(line)

        print(self.config)

    def displayWorkersRecap(self):
        totalWaitingTime = totalServingTime = totalWorkingTime = 0
        averageWaitingTime = averageServingTime = averageWorkingTime = 0

        for worker in self.workers:
            totalWaitingTime += worker.waitingTime
            totalServingTime += worker.servingTime
            totalWorkingTime += worker.workingTime
    
        totalWaitingTime += self.memo.waitingTimeDone
        totalServingTime += self.memo.servingTimeDone
        totalWorkingTime += self.memo.workingTimeDone

        totalWorkers = (float)(len(self.workers) + self.memo.workersDone)

        if (totalWorkers > 0):
            averageWaitingTime += (float)(totalWaitingTime) / totalWorkers
            averageServingTime += (float)(totalServingTime) / totalWorkers
            averageWorkingTime += (float)(totalWorkingTime) / totalWorkers 

        print(line)
        print('Workers Recap')
        print(line)
        
        print('Total: %d\nAverageWaitingTime: %f\nAverageServingTime: %f\nAverageWorkingTime: %f\n'
            % (totalWorkers, averageWaitingTime, averageServingTime, averageWorkingTime), end = '')
        
    def displayElevatorsRecap(self):

        totalWaitingTime = totalServingTime = totalWorkingTime = 0
        averageWaitingTime = averageServingTime = averageWorkingTime = 0

        for elevator in self.elevators:
            totalWaitingTime += elevator.waitingTime
            totalServingTime += elevator.servingTime
    
        totalWaitingTime += self.memo.waitingTimeDone
        totalServingTime += self.memo.servingTimeDone
        totalWorkingTime += self.memo.workingTimeDone

        totalElevators = len(self.elevators)

        averageWaitingTime += (float)(totalWaitingTime) / totalElevators
        averageServingTime += (float)(totalServingTime) / totalElevators
        averageWorkingTime += (float)(totalWorkingTime) / totalElevators 

        print(line)
        print('Elevators Recap')
        print(line)
        
        print('Total: %d\nAverageWaitingTime: %f\nAverageServingTime: %f\n'
            % (totalElevators, averageWaitingTime, averageServingTime), end = '')