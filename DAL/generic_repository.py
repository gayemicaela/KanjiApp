from abc import ABCMeta, abstractmethod

#abstractmethod: método que esta declarado en una clase pero no tiene implementación
# Las clases que heredan de esta clase deben proporcionar su propia implementación.

class GenericRepository(metaclass=ABCMeta):
    
    @abstractmethod
    def read(self):
        pass