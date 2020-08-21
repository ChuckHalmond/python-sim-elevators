import yaml
import inspect

class Config(yaml.YAMLObject):
    """
        The Configuration parameters of the simulation.
    """
    yaml_tag = '!Config'

    def __init__(self, live: bool, liveDelay: int, recap: bool, steps: int,
    randSeed: int, mu: float, lbda: float, floors: int, elevators: int, capacity: int,
    scheduling: str, idle: str):
        self.live = live
        self.liveDelay = liveDelay        
        self.recap = recap
        self.steps = steps

        self.randSeed = randSeed
        self.mu = mu
        self.lbda = lbda

        self.floors = floors
        self.elevators = elevators
        self.capacity = capacity
        self.scheduling = scheduling
        self.idle = idle

    def partialOverride(self, partialConfig):
        self.live = self.live if not hasattr(partialConfig, 'live') else partialConfig.live
        self.liveDelay = self.liveDelay if not hasattr(partialConfig, 'liveDelay') else partialConfig.liveDelay
        self.recap = self.recap if not hasattr(partialConfig, 'recap') else partialConfig.recap
        self.steps = self.steps if not hasattr(partialConfig, 'steps') else partialConfig.steps
        self.randSeed = self.randSeed if not hasattr(partialConfig, 'randSeed') == None else partialConfig.randSeed
        self.mu = self.mu if not hasattr(partialConfig, 'mu') == None else partialConfig.mu
        self.lbda = self.lbda if not hasattr(partialConfig, 'lbda') else partialConfig.lbda
        self.floors = self.floors if not hasattr(partialConfig, 'floors') else partialConfig.floors
        self.elevators = self.elevators if not hasattr(partialConfig, 'elevators') else partialConfig.elevators
        self.capacity = self.capacity if not hasattr(partialConfig, 'capacity') else partialConfig.capacity
        self.scheduling = self.scheduling if not hasattr(partialConfig, 'scheduling') else partialConfig.scheduling
        self.idle = self.idle if not hasattr(partialConfig, 'idle') else partialConfig.idle
    
    def __repr__(self):
        return ('%s(live=%r, liveDelay=%r, recap=%r, steps=%r, randSeed=%r, '
            'mu=%r, lbda=%r, floors=%r, elevators=%r, capacity=%r, scheduling=%r, idle=%r)') % (
            self.__class__.__name__, self.live, self.liveDelay, self.recap, self.steps,
            self.randSeed, self.mu, self.lbda, self.floors, self.elevators, self.capacity,
            self.scheduling, self.idle
            )