from abc import ABC, abstractmethod


class Report(ABC):
    @abstractmethod
    def generate(self, data):
        pass