from flask import jsonify


class ErrorHandling:
    """
    Error handling class for the FlaskAPI class
    rollback: Rollback the database to the previous state preventing any crashes

    duplicateTableError: Table already exist
    undefinedTableError: Table does not exist
    duplicateColumnError: Column already exist
    undefinedColumnError: Column does not exist
    undefinedObjectError: Invalid type
    typeConversionError: Existing column data is incompatible with prospect data

    :param args: tuple
    :param kwargs: dict

    :return: dict
    """

    def __init__(self, *args, **kwargs):
        self.rollback = kwargs.get('rollback')

    def duplicateTableError(self, table: str) -> jsonify:
        self.rollback()
        return {"status": 500, "error": f"Table already exist: {table}"}

    def undefinedTableError(self, table: str) -> jsonify:
        self.rollback()
        return {"status": 500, "error": f"Table does not exist: {table}"}

    def duplicateColumnError(self, column: str) -> jsonify:
        self.rollback()
        return {"status": 500, "error": f"Column already exist: {column}"}

    def undefinedColumnError(self, column: str) -> jsonify:
        self.rollback()
        return {"status": 500, "error": f"Column does not exist: {column}"}

    def undefinedObjectError(self, column_type: str) -> jsonify:
        self.rollback()
        return {"status": 500, "error": f"Invalid type: {column_type}"}

    def typeConversionError(self, column_type: str) -> jsonify:
        self.rollback()
        return {"status": 500, "error": f"Existing column data is incompatible with prospect data type: {column_type}"}

    def inFailedSqlTransactionError(self) -> jsonify:
        self.rollback()
        return {"status": 500, "error": "Failed to execute SQL transaction"}

    def syntaxError(self) -> jsonify:
        self.rollback()
        return {"status": 500, "error": "Syntax error: Invalid url or parameters"}
