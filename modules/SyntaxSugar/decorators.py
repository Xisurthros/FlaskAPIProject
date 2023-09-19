from typing import Callable


def convertTableNameToLower(func: Callable) -> Callable:
    """
    Table names are case seem to be set to all lower case base on my testing with requests specifically
    Convert all keys in a dict to lowercase

    :param func: function
    """

    def wrapper(*args, **kwargs):
        """
        :param args: tuple
        :param kwargs: dict
        :return: dict
        """
        try:
            data = kwargs.get('data')
            if data['table_name']:
                data['table_name'] = data['table_name'].lower()
            return func(*args, **kwargs)
        except TypeError:
            return func(*args, **kwargs)

    return wrapper


def convertColumnNameToLower(func: Callable) -> Callable:
    """
    Column names are case seem to be set to all lower case base on my testing with requests specifically
    Convert all keys in a dict to lowercase

    :param func: function
    """

    def wrapper(*args, **kwargs):
        """
        :param args: tuple
        :param kwargs: dict
        :return: dict
        """
        data = kwargs.get('data')
        keyList = [key for key in data.keys()]
        if 'column_name' in keyList:
            data['column_name'] = data['column_name'].lower()
        if 'new_column_name' in keyList:
            data['new_column_name'] = data['new_column_name'].lower()
        if 'column_type' in keyList:
            data['column_type'] = data['column_type'].lower()
        if 'row_data' in keyList:
            data['row_data']['column_name'] = data['row_data']['column_name'].lower()
            data['row_data']['column_type'] = data['row_data']['column_type'].lower()
        return func(*args, **kwargs)

    return wrapper
