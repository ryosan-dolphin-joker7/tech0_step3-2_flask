from flask import Flask, request
from flask import jsonify
import json
from flask_cors import CORS

from db_control import crud, mymodels

import requests

from dotenv import load_dotenv
import os

# .env ファイルを読み込みます
load_dotenv()

# 環境変数の使用
api_endpoint = os.getenv('API_ENDPOINT')

print(api_endpoint)

# Azure Database for MySQL
# REST APIでありCRUDを持っている
app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "<p>Flask top page!</p>"

@app.route("/customers", methods=['POST'])
def create_customer():
    values = request.get_json()
    # values = {
    #     "customer_id": "C005",
    #     "customer_name": "佐藤Aこ",
    #     "age": 64,
    #     "gender": "女"
    # }
    tmp = crud.myinsert(mymodels.Customers, values)
    result = crud.myselect(mymodels.Customers, values.get("customer_id"))
    return result, 200

@app.route("/customers", methods=['GET'])
def read_one_customer():
    model = mymodels.Customers
    target_id = request.args.get('customer_id') #クエリパラメータ
    result = crud.myselect(mymodels.Customers, target_id)
    return result, 200

@app.route("/allcustomers", methods=['GET'])
def read_all_customer():
    model = mymodels.Customers
    result = crud.myselectAll(mymodels.Customers)
    return result, 200

@app.route("/customers", methods=['PUT'])
def update_customer():
    try:
        print("I'm in")
        values = request.get_json()
        if not values:
            print("Invalid JSON payload")
            return jsonify({"error": "Invalid JSON payload"}), 400

        values_original = values.copy()
        model = mymodels.Customers

        print("Updating customer with values:", values)
        try:
            tmp = crud.myupdate(model, values)
        except Exception as e:
            print("Update failed:", str(e))
            return jsonify({"error": f"Update failed: {str(e)}"}), 500

        print("Fetching updated customer")
        try:
            result = crud.myselect(mymodels.Customers, values_original.get("customer_id"))
        except Exception as e:
            print("Select failed:", str(e))
            return jsonify({"error": f"Select failed: {str(e)}"}), 500

        return result, 200
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/customers", methods=['DELETE'])
def delete_customer():
    model = mymodels.Customers
    target_id = request.args.get('customer_id') #クエリパラメータ
    result = crud.mydelete(model, target_id)
    return result, 200

@app.route("/fetchtest")
def fetchtest():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    return response.json(), 200
