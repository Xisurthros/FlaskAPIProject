from flask import Flask, request
from modules.classes.FlaskAPI import FlaskAPI

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object('config')
limiter = Limiter(get_remote_address, app=app, default_limits=["86400 per day", "3600 per hour"], storage_uri='memory://')


@app.route('/api/v1/tables', methods=['GET'])
@limiter.limit("1/second")
def get_tables():
    return api.get_tables(api_key=request.headers.get('x-api-key'))


@app.route('/api/v1/create-table', methods=['GET', 'POST'])
@limiter.limit("1/second")
def create_table():
    return api.create_table(api_key=request.headers.get('x-api-key'), data=request.get_json())


@app.route('/api/v1/delete-table', methods=['GET', 'POST'])
@limiter.limit("1/second")
def delete_table():
    return api.delete_table(api_key=request.headers.get('x-api-key'), data=request.get_json())


@app.route('/api/v1/columns', methods=['GET', 'POST'])
@limiter.limit("1/second")
def get_columns():
    return api.get_columns(api_key=request.headers.get('x-api-key'), data=request.get_json())


@app.route('/api/v1/create-column', methods=['GET', 'POST'])
@limiter.limit("1/second")
def create_column():
    return api.create_column(api_key=request.headers.get('x-api-key'), data=request.get_json())


@app.route('/api/v1/delete-column', methods=['GET', 'POST'])
@limiter.limit("1/second")
def delete_column():
    return api.delete_column(api_key=request.headers.get('x-api-key'), data=request.get_json())


@app.route('/api/v1/update-column-name', methods=['GET', 'POST'])
@limiter.limit("1/second")
def update_column_name():
    return api.update_column_name(api_key=request.headers.get('x-api-key'), data=request.get_json())


@app.route('/api/v1/update-column-type', methods=['GET', 'POST'])
@limiter.limit("1/second")
def update_column_type():
    return api.update_column_type(api_key=request.headers.get('x-api-key'), data=request.get_json())


@app.route('/api/v1/rows', methods=['GET', 'POST'])
@limiter.limit("1/second")
def get_rows():
    return api.get_rows(api_key=request.headers.get('x-api-key'), data=request.get_json())


@app.route('/api/v1/insert-row', methods=['GET', 'POST'])
@limiter.limit("1/second")
def insert_row():
    return api.insert_row(api_key=request.headers.get('x-api-key'), data=request.get_json())


@app.route('/api/v1/select-row', methods=['GET', 'POST'])
@limiter.limit("1/second")
def select_row():
    return api.select_row(api_key=request.headers.get('x-api-key'), data=request.get_json())


@app.route('/api/v1/update-row', methods=['GET', 'POST'])
@limiter.limit("1/second")
def update_row():
    return api.update_row(api_key=request.headers.get('x-api-key'), data=request.get_json())


@app.route('/api/v1/delete-row', methods=['GET', 'POST'])
@limiter.limit("1/second")
def delete_row():
    return api.delete_row(api_key=request.headers.get('x-api-key'), data=request.get_json())


if __name__ == '__main__':
    api = FlaskAPI()
    app.run()
