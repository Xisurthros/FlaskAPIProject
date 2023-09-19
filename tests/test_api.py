import csv
import time
import requests


class testFlaskAPI:
    """
    Testing FlaskAPI before switching to Postman
    Incomplete file as all tests have been created on Postman
    Checkout: FlaskAPI.postman_collection.json
    """

    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}

    def create_table(self):
        """
        Creates a table in the database

        :return:
        """

        data = {"table_name": "pokemon_jhobbs"}
        response = requests.post("http://127.0.0.1:5000/api/v1/create-table", headers=self.headers, json=data)
        print(response.text)

    def delete_table(self):
        """
        Deletes a table in the database

        :return:
        """

        data = {"table_name": "pokemon_jhobbs"}
        response = requests.delete("http://127.0.0.1:5000/api/v1/delete-table", headers=self.headers, json=data)
        print(response.text)

    def insert_row(self):
        """
        Inserts a row into a table in the database

        :return:
        """

        data = {"table_name": "pokemon_jhobbs",
                "row_data": {"pokemon_number": "5", "pokemon_name": "Testing5", "pokemon_type": "Grass",
                             "notes": 'Please Work'}}
        response = requests.get("http://127.0.0.1:5000/api/v1/insert-row", headers=self.headers, json=data)
        print(response.text)

    def get_columns(self):
        """
        Gets all columns in a table

        :return:
        """

        data = {"table_name": "pokemon_jhobbs"}
        response = requests.get("http://127.0.0.1:5000/api/v1/columns", headers=self.headers, json=data)
        print(response.text)

    def create_column(self):
        """
        Creates a column in a table

        :return:
        """

        data = {"table_name": "pokemon_jhobbs", "column_name": "AHHHHHH", "column_type": "integer"}
        response = requests.get("http://127.0.0.1:5000/api/v1/create-column", headers=self.headers, json=data)
        print(response.text)

    def select_row(self):
        """
        Selects a row in a table

        :return:
        """

        data = {"table_name": "pokemon_jhobbs", "column_name": "pokemon_name", "column_value": "Testing5"}
        response = requests.get('http://127.0.0.1:5000/api/v1/select-row', headers=self.headers, json=data)
        print(response.text)

    def addPokemonToDatabase(self):
        x = 0
        with open('pokemon.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if x == 0:
                    x += 1
                else:
                    data = {"table_name": "pokemon_jhobbs",
                            "row_data": {"pokemon_number": row[0].replace("'", '').replace("#", ''), "pokemon_name": row[1].replace("'", ''),
                                         "pokemon_type": row[2].replace("'", "").replace("[", "")
                                         .replace("]", ""), "notes": row[3]}}
                    print(data)
                    response = requests.post("http://127.0.0.1:5000/api/v1/insert-row", headers=self.headers, json=data)
                    print(response.text)
                    time.sleep(0.25)


def main():
    test.addPokemonToDatabase()


if __name__ == '__main__':
    test = testFlaskAPI()
    main()
