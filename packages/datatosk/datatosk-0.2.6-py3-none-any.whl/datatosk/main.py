from typing import Callable

from . import engines


class Source:
    """
    Main interface of datatosk.

    Examples:
        >>> import datatosk
        >>> source = datatosk.Source.mysql(source_name="local")
        >>> source.read("SELECT * FROM table")
           col1  col2
        0     1     3
        1     2     4
    """

    mysql: Callable = engines.MySQLEngine
    gbq: Callable = engines.GoogleBigQueryEngine
    pickle: Callable = engines.PickleEngine
