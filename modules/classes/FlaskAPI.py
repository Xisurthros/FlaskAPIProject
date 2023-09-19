import os
import psycopg2
from flask import jsonify
from modules.classes.ErrorHandling import ErrorHandling
from modules.classes.SuccessMessages import SuccessMessage
from modules.security.Authentication import Authentication
from modules.security.Authentication import invalidAPIKeyError
from modules.SyntaxSugar.decorators import convertTableNameToLower
from modules.SyntaxSugar.decorators import convertColumnNameToLower


class FlaskAPI(ErrorHandling, SuccessMessage, Authentication):
    """
    rollback: Rollback the database to the previous state preventing any crashes
    conn: Database connection
    cur: Database cursor

    *** Database functions ***
    get_tables: Get all tables in the database
    create_table: Create a new table in the database
    delete_table: Delete a table in the database
    add_column: Add a column to a table in the database
    delete_column: Delete a column from a table in the database
    update_column: Update a column in a table in the database
    add_row: Add a row to a table in the database
    select_row: Select a row from a table in the database
    insert_row: Insert a row into a table in the database
    delete_row: Delete a row from a table in the database
    update_row: Update a row in a table in the database

    *** Other ***
    All functions require api_key, IDEs don't show api_key being used but the variable is used in the wrapper function in __getattribute__
    """

    def __init__(self):
        self.conn = psycopg2.connect(
            database=os.environ.get("POSTGRES_DB"),
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            host=os.environ.get("POSTGRES_HOST"),
            port=os.environ.get("POSTGRES_PORT")
        )
        self.cur = self.conn.cursor()
        self.rollback = self.cur.connection.rollback
        super(FlaskAPI, self).__init__(rollback=self.rollback)
        SuccessMessage.__init__(self)
        Authentication.__init__(self)

    def __getattribute__(self, attr: str) -> object:
        """
        Verify the API key passed from the user is valid before executing any function in the class

        :param attr: Attribute to get
        :return: object
        """

        attribute = object.__getattribute__(self, attr)

        # Get all functions in the FlaskAPI class
        allowedAttributes = [func for func in dir(__class__.__name__) if callable(getattr(__class__.__name__, func)) and not any(x in func for x in ['__', 'success', 'Error', 'api'])]

        if callable(attribute) and attribute.__name__ in allowedAttributes:
            def wrapper(*args, **kwargs) -> object:
                """
                Wrapper function to check the API key before executing the function

                :param args: args[0] is the API key passed from the user
                :param kwargs: kwargs['api_key'] is the API key passed from the user
                :return: object
                """

                if self.check_api_key(api_key=kwargs.get('api_key')):
                    return attribute(*args, **kwargs)
                else:
                    return invalidAPIKeyError()

            return wrapper
        return object.__getattribute__(self, attr)

    # TODO: Test response when no tables exist
    #       Unable to test with current Postgres database without delete other users tables
    #       Test with a new database
    def get_tables(self, api_key: str) -> jsonify:
        """
        Get all tables in the database

        :param api_key: API key from the request header, used to authenticate the user in __getattribute__()
        :return: JSON list of tables
        """

        try:
            self.cur.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public'")
            tables = self.cur.fetchall()

            tablesJSON = []
            for table in tables:
                tableJSON = {
                    "table_schema": table[1],
                    "table_name": table[2],
                    "table_type": table[3]
                }
                tablesJSON.append(tableJSON)
            return jsonify(tablesJSON)
        except psycopg2.errors.InFailedSqlTransaction:
            return self.inFailedSqlTransactionError()

    @convertTableNameToLower
    def create_table(self, api_key: str, data: dict) -> jsonify:
        """
        Create a new table in the database

        :param api_key: API key from the request header, used to authenticate the user in __getattribute__()
        :param data: {"table_name": "table_name"}
        :return: {"success": "Message"}
        """

        try:
            self.cur.execute(f"CREATE TABLE {data['table_name']} (id SERIAL PRIMARY KEY)")
            self.conn.commit()
            return self.success("create_table", data={"table_name": data['table_name']})
        except psycopg2.errors.DuplicateTable:
            return self.duplicateTableError(data['table_name'])
        except psycopg2.errors.SyntaxError:
            return self.syntaxError()

    @convertTableNameToLower
    def delete_table(self, api_key: str, data: dict) -> jsonify:
        """
        Delete a table in the database

        :param api_key: API key from the request header, used to authenticate the user in __getattribute__()
        :param data: {"table_name": "table_name"}
        :return: {"success": "Message"}
        """

        try:
            self.cur.execute(f"DROP TABLE {data['table_name']}")
            self.conn.commit()
            return self.success("delete_table", data={"table_name": data['table_name']})
        except psycopg2.errors.UndefinedTable:
            return self.undefinedTableError(data['table_name'])
        except psycopg2.errors.SyntaxError:
            return self.syntaxError()

    @convertTableNameToLower
    def get_columns(self, api_key: str, data: dict) -> jsonify:
        """
        Get all columns in a table

        :param api_key: API key from the request header, used to authenticate the user in __getattribute__()
        :param data: {"table_name": "table_name"}
        :return: JSON list of columns
        """

        try:
            self.cur.execute(f"SELECT * FROM information_schema.columns WHERE table_name = '{data['table_name']}'")
            columns = self.cur.fetchall()

            # If no columns are found, check if the table exists
            if len(columns) == 0:
                self.cur.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public'")
                tables = self.cur.fetchall()

                if data["table_name"] not in [table[2] for table in tables]:
                    raise psycopg2.errors.UndefinedTable

            else:
                columnsJSON = []
                for column in columns:
                    columnJSON = {
                        "column_name": column[3],
                        "column_order": column[4],
                        "column_type": column[7]
                    }
                    columnsJSON.append(columnJSON)
                return jsonify(columnsJSON)
        except psycopg2.errors.UndefinedTable:
            return self.undefinedTableError(data["table_name"])

    @convertTableNameToLower
    @convertColumnNameToLower
    def create_column(self, api_key: str, data: dict) -> jsonify:
        """
        Create a column in a table

        :param api_key: API key from the request header, used to authenticate the user in __getattribute__()
        :param data: {"table_name": "table_name", "column_name": "column_name", "column_type": "column_type"}
        :return: {"success": "Message"}
        """

        try:
            self.cur.execute(f"ALTER TABLE {data['table_name']} ADD COLUMN {data['column_name']} {data['column_type']}")
            self.conn.commit()
            return self.success("create_column", {"table_name": data['table_name'], "column_name": data['column_name']})
        except psycopg2.errors.UndefinedTable:
            return self.undefinedTableError(data['table_name'])
        except psycopg2.errors.DuplicateColumn:
            return self.duplicateColumnError(data['column_name'])
        except psycopg2.errors.UndefinedObject:
            return self.undefinedObjectError(data['column_type'])
        except psycopg2.errors.SyntaxError:
            return self.syntaxError()

    @convertTableNameToLower
    @convertColumnNameToLower
    def delete_column(self, api_key: str, data: dict) -> jsonify:
        """
        Delete a column in a table

        :param api_key: API key from the request header, used to authenticate the user in __getattribute__()
        :param data: {"table_name": "table_name", "column_name": "column_name"}
        :return: {"success": "Message"}
        """

        try:
            self.cur.execute(f"ALTER TABLE {data['table_name']} DROP COLUMN {data['column_name']}")
            self.conn.commit()
            return self.success("delete_column", data={"table_name": data['table_name'], "column_name": data['column_name']})
        except psycopg2.errors.UndefinedTable:
            return self.undefinedTableError(data['table_name'])
        except psycopg2.errors.UndefinedColumn:
            return self.undefinedColumnError(data['column_name'])
        except psycopg2.errors.SyntaxError:
            return self.syntaxError()

    @convertTableNameToLower
    @convertColumnNameToLower
    def update_column_name(self, api_key: str, data: dict) -> jsonify:
        """
        Update a column name in a table

        :param api_key: API key from the request header, used to authenticate the user in __getattribute__()
        :param data: {"table_name": "table_name", "column_name": "column_name", "new_column_name": "new_column_name"}
        :return: {"success": "Message"}
        """

        try:
            self.cur.execute(f"ALTER TABLE {data['table_name']} RENAME COLUMN {data['column_name']} TO {data['new_column_name']}")
            self.conn.commit()
            return self.success("update_column_name", data={"table_name": data['table_name'], "column_name": data['column_name'], "new_column_name": data['new_column_name']})
        except psycopg2.errors.UndefinedTable:
            return self.undefinedTableError(data['table_name'])
        except psycopg2.errors.UndefinedColumn:
            return self.undefinedColumnError(data['column_name'])
        except psycopg2.errors.DuplicateColumn:
            return self.duplicateColumnError(data['column_name'])
        except psycopg2.errors.SyntaxError:
            return self.syntaxError()

    @convertTableNameToLower
    @convertColumnNameToLower
    def update_column_type(self, api_key: str, data: dict) -> jsonify:
        """
        Update a column type in a table

        :param api_key: API key from the request header, used to authenticate the user in __getattribute__()
        :param data: {"table_name": "table_name", "column_name": "column_name", "new_column_type": "new_column_type"}
        :return: {"success": "Message"}
        """

        try:
            self.cur.execute(f"ALTER TABLE {data['table_name']} ALTER COLUMN {data['column_name']} TYPE {data['new_column_type']} USING {data['column_name']}::{data['new_column_type']}")
            self.conn.commit()
            return self.success("update_column_type", data={"table_name": data['table_name'], "column_name": data['column_name'], "new_column_type": data['new_column_type']})
        except psycopg2.errors.UndefinedTable:
            return self.undefinedTableError(data['table_name'])
        except psycopg2.errors.UndefinedColumn:
            return self.undefinedColumnError(data['column_name'])
        except psycopg2.errors.DuplicateColumn:
            return self.duplicateColumnError(data['column_name'])
        except psycopg2.errors.SyntaxError:
            return self.syntaxError()
        # TODO: Fix this
        #     : This is a gross way of getting all possible type conversion errors
        except Exception as e:
            return self.typeConversionError(str(e).split(' ')[5].replace(':', ''))

    @convertTableNameToLower
    def get_rows(self, api_key: str, data: dict) -> jsonify:
        """
        Get rows from a table

        :param api_key: API key from the request header, used to authenticate the user in __getattribute__()
        :param data: {"table_name": "table_name"}
        :return: {"success": "Message", "data": [{"column_name": "column_value"}]}
        """

        try:
            columns = [header["column_name"] for header in sorted(self.get_columns(api_key, data).json, key=lambda d: d['column_order'])]
            self.cur.execute(f"SELECT * FROM {data['table_name']}")
            self.conn.commit()
            return [dict(zip(columns, row)) for row in self.cur.fetchall()]
        except psycopg2.errors.UndefinedTable:
            return self.undefinedTableError(data['table_name'])
        except psycopg2.errors.SyntaxError:
            return self.syntaxError()

    @convertTableNameToLower
    def insert_row(self, api_key: str, data: dict) -> jsonify:
        """
        Insert a row into a table

        :param api_key: API key from the request header, used to authenticate the user in __getattribute__()
        :param data: {"table_name": "table_name", "row_data": {"column_name": "column_value"}}
        :return: {"success": "Message"}
        """

        try:
            table_name = data["table_name"]
            data.pop("table_name")

            columns = ", ".join(data['row_data'].keys())
            values = ", ".join([f"'{value}'" for value in data['row_data'].values()])

            self.cur.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
            self.conn.commit()
            return self.success("insert_row", {"table_name": table_name, 'data': data})
        except psycopg2.errors.UndefinedTable:
            return self.undefinedTableError(data["table_name"])
        except psycopg2.errors.UndefinedColumn as e:
            return self.undefinedColumnError(str(e).split(" ")[1].strip('"'))
        except psycopg2.errors.SyntaxError:
            return self.syntaxError()

    @convertTableNameToLower
    @convertColumnNameToLower
    def select_row(self, api_key: str, data: dict) -> jsonify:
        """
        Select a row from a table

        :param api_key: API key from the request header, used to authenticate the user in __getattribute__()
        :param data: {"table_name": "table_name", "column_name": "column_name", "column_value": "column_value"}
        :return: {"success": "Message", "data": [{"column_name": "column_value"}]}
        """

        try:
            columns = [header["column_name"] for header in sorted(self.get_columns(api_key, data).json, key=lambda d: d['column_order'])]
            self.cur.execute(f"SELECT * FROM {data['table_name']} WHERE {data['column_name']} LIKE '%{data['column_value']}%'")
            self.conn.commit()
            return [dict(zip(columns, row)) for row in self.cur.fetchall()]
        except psycopg2.errors.UndefinedTable:
            return self.undefinedTableError(data['table_name'])
        except psycopg2.errors.UndefinedColumn as e:
            return self.undefinedColumnError(str(e).split(" ")[1].strip('"'))
        except psycopg2.errors.SyntaxError:
            return self.syntaxError()

    @convertTableNameToLower
    def update_row(self, api_key: str, data: dict) -> jsonify:
        """
        Update a specific row in a table

        :param api_key: API key from the request header, used to authenticate the user in __getattribute__()
        :param data: {"table_name": "table_name", "row_id": "row_id", "new_row_data": {"column_name": "column_value"}}
        :return: {"success": "Message"}
        """

        try:
            table_name = data["table_name"]
            data.pop("table_name")

            row_id = data["row_id"]
            data.pop("row_id")

            columns = ", ".join(data["new_row_data"].keys())
            values = ", ".join([f"'{value}'" for value in data["new_row_data"].values()])

            self.cur.execute(f"UPDATE {table_name} SET ({columns}) = ({values}) WHERE id = {row_id}")
            self.conn.commit()
            return self.success("update_row", {'table_name': table_name, 'data': data})
        except psycopg2.errors.UndefinedTable:
            return self.undefinedTableError(data["table_name"])
        except psycopg2.errors.UndefinedColumn as e:
            return self.undefinedColumnError(str(e).split(" ")[1].strip('"'))
        except psycopg2.errors.SyntaxError:
            return self.syntaxError()

    @convertTableNameToLower
    def delete_row(self, api_key: str, data: dict) -> jsonify:
        """
        Delete a specific row in a table

        :param api_key: API key from the request header, used to authenticate the user in __getattribute__()
        :param data: {"table_name": "table_name", "row_id": "row_id"}
        :return: {"success": "Message"}
        """

        try:
            self.cur.execute(f"DELETE FROM {data['table_name']} WHERE id = {data['row_id']}")
            self.conn.commit()
            return self.success("delete_row", {"table_name": data['table_name'], 'row_id': data['row_id'], 'data': data})
        except psycopg2.errors.UndefinedTable:
            return self.undefinedTableError(data['table_name'])
        except psycopg2.errors.UndefinedColumn as e:
            return self.undefinedColumnError(str(e).split(" ")[1].strip('"'))
        except psycopg2.errors.SyntaxError:
            return self.syntaxError()
