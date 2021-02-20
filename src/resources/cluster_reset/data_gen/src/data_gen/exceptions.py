class DataGenException(Exception):
    """ A module-specific exception """


class NoTablesInKeyspace(DataGenException):
    """ No tables were found in the provided keyspace """
