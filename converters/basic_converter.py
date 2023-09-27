from abc import ABC, abstractmethod

class BasicConverter(ABC):
    # @abstractmethod
    # def __init__(self):
    #     pass

    @abstractmethod
    def _process(self):
        pass

    @abstractmethod
    def convert_data(self, data):
        pass
