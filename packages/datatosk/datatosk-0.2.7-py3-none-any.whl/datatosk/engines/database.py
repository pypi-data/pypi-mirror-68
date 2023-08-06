from abc import ABCMeta, abstractmethod
from contextlib import closing
from os import getenv
from typing import List, Any, Union, Dict, Callable

import MySQLdb  # type: ignore
import pandas as pd  # type: ignore
import pandas_gbq  # type: ignore

from .. import consts


class _DataBaseEngine(metaclass=ABCMeta):

    """
    Abstract class from which all database engine classes inherit.
    
    Derived classes must implement `__init__()` and `query()` and `update()` methods.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def read(self, query: str, output_type: str = consts.output_types.PANDAS, **kwargs):
        """
        Abstract method which is used as interface for retrieving data from databases.

        Args:
            query: query string for extracting data.
            output_type: type of an object which will be output from query operation.
        """

    @abstractmethod
    def write(self, obj: Any):
        """
        Abstract method which is used as interface for sending data to sources.
        """


class MySQLEngine(_DataBaseEngine):

    """
    Class that enables to connect to MySQL database and retrieve data from it.

    Attributes:
        host: MySQL host needed to connect to database.
        port: MySQL port needed to connect to database.
        user: MySQL user needed to connect to database.
        password: MySQL password needed to connect to database.
        database: MySQL database needed to connect to database.
    """

    def __init__(self, source_name: str):
        # TODO: As more use cases arise, move configuration to a separate module.

        super().__init__()

        self.host = getenv(f"MYSQL_{source_name}_HOST".upper())
        self.port = int(getenv(f"MYSQL_{source_name}_PORT".upper(), "3306"))
        self.user = getenv(f"MYSQL_{source_name}_USER".upper())
        self.password = getenv(f"MYSQL_{source_name}_PASS".upper())
        self.database = getenv(f"MYSQL_{source_name}_DB".upper())

    def read(
        self, query: str, output_type: str = consts.output_types.PANDAS, **kwargs
    ) -> Union[pd.DataFrame, list, dict]:
        """
        Fetches data from a MySQL.

        Args:
            query: query string for extracting data.
            output_type: type of an object which will be output from query operation.
            kwargs: when `output_type="pandas"` kwargs will be transfered to `pd.read_sql`

        Raises:
            NotImplementedError: An error occurred when not supported `output_type`.
        """

        output_type_map: Dict[str, Callable] = {
            consts.output_types.PANDAS: self._output_pandas,
            consts.output_types.LIST: self._output_list,
            consts.output_types.DICT: self._output_dict,
        }

        connection = MySQLdb.connect(
            self.host,
            self.user,
            self.password,
            self.database,
            self.port,
            charset="utf8",
        )

        try:
            return output_type_map[output_type](query, connection, **kwargs)
        except KeyError:
            raise TypeError(f"possible output_types: {list(output_type_map.keys())}")

    def write(self, obj: Any):
        """
        [TODO]
        """
        raise NotImplementedError

    @staticmethod
    def _output_pandas(
        query: str, connection: MySQLdb.Connection, **kwargs
    ) -> pd.DataFrame:
        """
        Outputs data from a MySQL query in pandas DataFrame object.

        Args:
            query: query string for extracting data.
            connection: MySQLdb.Connection object.

        Returns:
            pandas.DataFrame with queried data.
        """
        cursor = connection.cursor()
        with closing(cursor):
            return pd.read_sql(query, con=connection, **kwargs)

    @staticmethod
    def _output_list(query: str, connection: MySQLdb.Connection) -> list:
        """
        Outputs data from a MySQL query in a list.

        Args:
            query: query string for extracting data.
            connection: MySQLdb.Connection object.

        Returns:
            One element list if one column selected, otherwise nested list.
        """
        cursor = connection.cursor()
        with closing(cursor):
            cursor.execute(query)

            return [
                item[0] if len(item) == 1 else list(item) for item in cursor.fetchall()
            ]

    @staticmethod
    def _output_dict(query: str, connection: MySQLdb.Connection) -> List[dict]:
        """
        Outputs data from a MySQL query in a list of dicts.

        Args:
            query: query string for extracting data.
            connection: MySQLdb.Connection object.

        Returns:
            List of dictionaries in which keys are column names.
        """
        cursor = connection.cursor()
        with closing(cursor):
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]

            return [dict(zip(columns, row)) for row in cursor.fetchall()]


class GoogleBigQueryEngine(_DataBaseEngine):

    """
    Class that enables to connect to GoogleBigQuery database 
    and retrieve data from it.

    Attributes:
        project_id: GBQ project_id needed to connect to database.
    """

    def __init__(self, dataset: str):

        super().__init__()
        self.project_id = getenv(f"GBQ_{dataset}_PROJECT_ID".upper(), "")

    def read(self, query: str, output_type: str = consts.output_types.PANDAS, **kwargs):
        """
        Fetches data from a GoogleBigQuery.
        
        Args:
            query: query string for extracting data.
            output_type: type of an object which will be output from query operation.
        
        Returns:
            Queried data from GBQ database in type specified in `output_type".
        """

        output_type_mapper = {
            consts.output_types.PANDAS: self._output_pandas,
            consts.output_types.LIST: self._output_list,
            consts.output_types.DICT: self._output_dict,
        }
        try:
            return output_type_mapper[output_type](query, self.project_id)
        except KeyError:
            raise TypeError(f"possible output_types: {list(output_type_mapper.keys())}")

    def write(self, obj: Any):
        """
        [TODO]
        """
        raise NotImplementedError

    @staticmethod
    def _output_pandas(query: str, project_id: str) -> pd.DataFrame:
        """
        Outputs data from a GBQ query in pandas DataFrame object.

        Args:
            query: query string for extracting data.
            project_id: GBQ project_id string.

        Returns:
            pandas.DataFrame with queried data.
        """
        return pandas_gbq.read_gbq(query=query, project_id=project_id)

    @staticmethod
    def _output_list(query: str, project_id: str):
        """
        [TODO]

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    @staticmethod
    def _output_dict(query: str, project_id: str):
        """
        [TODO]

        Raises:
            NotImplementedError
        """

        raise NotImplementedError
