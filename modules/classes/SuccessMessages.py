from flask import jsonify


class SuccessMessage:

    def __init__(self):
        self.data = {}
        self.status = 200

    def success(self, attr: str, data: dict) -> jsonify:
        """
        Return a success message

        :param attr: str - The name of the function that called this method (ex: create_table, delete_table, etc.)
        :param data: dict - The data that was passed to the function that called this method
        :return: {"status": 200, "success": "Unique message"}
        """

        # Set default values for extra data not used in the specific success message
        self.data = data
        self.data.update({x: y for list_item in [{variable: ""} for variable in ['table_name', 'column_name', 'new_column_name', 'new_column_type', 'data'] if variable not in data] for (x, y) in list_item.items()})

        """
         These 4 lines are the simplified version of line 15
         But I left line 15 because I wanted to be obnoxious :) (╯°□°)╯︵ ┻━┻ blame Everett or something IDK

         variables = ['table_name', 'column_name', 'new_column_name', 'var_type', 'data']
         for variable in variables:
             if variable not in data:
                 data[variable] = ""
        """

        successMessages = {
            "create_table": {"status": self.status, "success": f"Table created successfully: {self.data['table_name']}"},
            "delete_table": {"status": self.status, "success": f"Table deleted successfully: {self.data['table_name']}"},
            "create_column": {"status": self.status, "success": f"Column: {self.data['column_name']} created in table: {self.data['table_name']} successfully"},
            "delete_column": {"status": self.status, "success": f"Column: {self.data['column_name']} deleted in table: {self.data['table_name']} successfully"},
            "update_column_name": {"status": self.status, "success": f"Column: {self.data['column_name']} updated name to: {self.data['new_column_name']} in table: {self.data['table_name']}"},
            "update_column_type": {"status": self.status, "success": f"Column: {self.data['column_name']} updated type to: {self.data['new_column_type']} in table: {self.data['table_name']}"},
            "insert_row": {"status": self.status, "success": f"Row inserted successfully in table: {self.data['table_name']}", "data": self.data['data']},
            "update_row": {"status": self.status, "success": f"Row updated successfully in table: {self.data['table_name']}", "data": self.data['data']},
            "delete_row": {"status": self.status, "success": f"Row deleted successfully in table: {data['table_name']}", "data": self.data['data']},
            "select_row": {"status": self.status, "success": f"Row selected successfully in table: {self.data['table_name']}", "data": self.data['data']}
        }
        return successMessages[attr]
