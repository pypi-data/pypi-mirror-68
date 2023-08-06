from typing import Callable

from . import engines


class Source:
    """
    Main interface of datatosk.

    Examples:
        Database:
        >>> import datatosk
        >>> source = datatosk.Source.mysql(source_name="local")
        >>> source.read("SELECT * FROM table")
           col1  col2
        0     1     3
        1     2     4
        File:
        >>> import datatosk
        >>> source = datatosk.Source.pickle(filepath="some_file.pickle")
        >>> source.read()
        Network:
        >>> import datatosk
        >>> source = datatosk.Source.requests(source_name="weather")
        >>> source.read(path="forecast/snowfall/")
    """

    mysql: Callable = engines.MySQLEngine
    gbq: Callable = engines.GoogleBigQueryEngine
    pickle: Callable = engines.PickleEngine
    requests: Callable = engines.RequestsEngine
