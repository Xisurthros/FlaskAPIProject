# FlaskAPI
## About
FlaskAPI is an API that allows the user to create, read, update, and delete data within a PostgreSQL database.

## Functionality
* [View, Create, Delete] tables in the database.
* [View, Create, Update, Delete] columns in a table.
* [View, Create, Select, Update, Delete] rows in a table.

## Paths

```python
get_tables = '/api/v1/tables'
create_table = '/api/v1/create-table'
delete_table = '/api/v1/delete-table'
get_columns = '/api/v1/columns'
create_column = '/api/v1/create-column'
delete_column = '/api/v1/delete-column'
update_column_name = '/api/v1/update-column-name'
update_column_type = '/api/v1/update-column-type'
get_rows = '/api/v1/rows'
insert_row = '/api/v1/insert-row'
select_row = '/api/v1/select-row'
update_row = '/api/v1/update-row'
delete_row = '/api/v1/delete-row'
```

## Data
```python
get_tables = None
create_table = {"table_name": "table_name"}
delete_table = {"table_name": "table_name"}
get_columns = {"table_name": "table_name"}
create_columns  = {"table_name": "table_name", "column_name": "column_name", "column_type": "column_type"}
delete_columns = {"table_name": "table_name", "column_name": "column_name"}
update_column_name = {"table_name": "table_name", "column_name": "column_name", "new_column_name": "new_column_name"}
update_column_type = {"table_name": "table_name", "column_name": "column_name", "new_column_type": "new_column_type"}
get_rows = {"table_name": "table_name"}
insert_row = {"table_name": "table_name", "row_data": {"column_name": "column_value"}}
select_row = {"table_name": "table_name", "row_id": "row_id"}
update_row = {"table_name": "table_name", "row_id": "row_id", "new_row_data": {"column_name": "column_value"}}
delete_row = {"table_name": "table_name", "row_id": "row_id"}
```

## Code Examples
```python
import requests

def main():
    # Create a table
    url = 'http://localhost:5000/api/v1/create-table'
    data = {'table_name': 'pokemon'}
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
               'x-api-key': '1234567890'}
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    
if __name__ == '__main__':
    main()
```
```terminal
Output: {"status": 200, "success": "Table created successfully: pokemon"}
```

## Future Updates
* Create multiple tables/columns/rows at once.
* Update data in multiple rows at once.
* Integrate a secondary database for unique user authentication. (Currently using a static API key)