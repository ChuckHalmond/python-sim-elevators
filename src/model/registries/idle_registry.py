from src.model.utils.singleton_meta import SingletonMeta

class IdleRegistry(metaclass = SingletonMeta):

    def __init__(self):
        self.dict = {}

    @staticmethod
    def register(tag, idle):
        IdleRegistry().dict[tag] = idle
    
    @staticmethod
    def get(tag):
        return IdleRegistry().dict.get(tag)

    @staticmethod
    def keys():
        return IdleRegistry().dict.keys()