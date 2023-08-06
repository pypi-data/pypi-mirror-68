from abc import abstractmethod, ABCMeta
from os import getenv
from typing import Any, Union, Dict, Callable

import requests

from .. import consts


class _NetworkEngine(metaclass=ABCMeta):
    """
    Abstract class from which all network engine classes inherit.

    Derived classes must implement `__init__()` and `read()` and `write()` methods.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def read(self, path: str, output_type: str = consts.output_types.DICT, **kwargs):
        """
        Abstract method which is used as interface for retrieving data via network.

        Args:
            path: Path component of the URL
            output_type: Object type which the request result will be transformed to.
        """

    @abstractmethod
    def write(self, obj: Any):
        """
        Abstract method which is used as interface for sending data to sources.
        """


class RequestsEngine(_NetworkEngine):
    """
    Class that enables to retrieve data via HTTP/HTTPS requests.

    Attributes:
        protocol: protocol needed to make a request.
        host: host needed to make a request.
        port: port needed to make a request.
    """

    def __init__(self, source_name: str):
        # TODO: As more use cases arise, move configuration to a separate module.

        super().__init__()

        self.protocol = getenv(f"HTTP_{source_name}_PROTOCOL".upper(), "http")
        self.host = getenv(f"HTTP_{source_name}_HOST".upper(), "localhost")
        self.port = getenv(f"HTTP_{source_name}_PORT".upper(), "80")

    def _url(self, path: str) -> str:
        """
        Provides a URL based on the end-point configuration.
        Args:
            path: The path component of the URL
        """
        return f"{self.protocol}://{self.host}:{self.port}/{path}"

    def read(
        self, path: str, output_type: str = consts.output_types.DICT, **kwargs
    ) -> Union[dict]:
        """
        Performs a request.

        Args:
            path: Path component of the URL
            output_type: type of an object which will be output from request.

        Raises:
            NotImplementedError: An error occurred when not supported `output_type`.
        """

        output_type_map: Dict[str, Callable] = {
            consts.output_types.DICT: self._output_dict,
        }

        response = requests.get(self._url(path), **kwargs)

        if not response.ok:
            raise HttpRequestFailedException(
                f"Server responded with status code {response.status_code}"
            )

        try:
            return output_type_map[output_type](response)
        except KeyError:
            raise TypeError(f"possible output_types: {list(output_type_map.keys())}")

    def write(self, obj: Any):
        raise NotImplementedError

    @staticmethod
    def _output_dict(response: requests.Response) -> dict:
        """
        Outputs data from a request response as a dict.

        Args:
            response: Response object

        Returns:
            One element list if one column selected, otherwise nested list.
        """
        return response.json()


class HttpRequestFailedException(Exception):
    """
    An exception raised when a HTTP request fails.
    """
