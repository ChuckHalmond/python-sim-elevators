from src.model.utils.singleton_meta import SingletonMeta

class SchedulingRegistry(metaclass = SingletonMeta):

    def __init__(self):
        self.dict = {}

    @staticmethod
    def register(tag, scheduling):
        SchedulingRegistry().dict[tag] = scheduling
    
    @staticmethod
    def get(tag):
        return SchedulingRegistry().dict.get(tag)
    
    @staticmethod
    def keys():
        return SchedulingRegistry().dict.keys()