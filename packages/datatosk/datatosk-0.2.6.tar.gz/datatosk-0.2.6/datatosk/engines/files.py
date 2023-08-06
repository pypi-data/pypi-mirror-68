from abc import ABC, abstractmethod
from typing import Union, Any
from pathlib import Path
import pickle


class _FileEngine(ABC):

    """
    Abstract class from which all file-based engine classes inherit.
    
    Derived classes must implement `__init__()`, `read()` and `write()` methods.
    """

    @abstractmethod
    def read(self):
        """
        Abstract method which is used as interface for retrieving data from files.
        """

    @abstractmethod
    def write(self, obj: Any):
        """
        Abstract method which is used as interface for sending data to sources.
        """


class PickleEngine(_FileEngine):
    
    """
    Class that enables to read and write to pickle files.

    Attributes:
        filepath: path string or Path object of file.
    """

    def __init__(self, filepath: Union[str, Path]):
      
        super().__init__()
        self.filepath = filepath

    def read(self) -> Any:
        """
        Fetches data from a pickle file.

        Returns:
            Object from pickle file
        """
        with open(self.filepath, "rb") as file:
            return pickle.load(file)

    def write(self, obj: Any):
        """
        Write Any object to pickle file.

        Args:
            obj: object to be pickled.
        """
        
        with open(self.filepath, 'wb') as file:
            pickle.dump(obj, file, protocol=pickle.HIGHEST_PROTOCOL)
