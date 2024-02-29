import os
import psycopg
from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.sort_keys = False

def db_conn():
    conn = psycopg.connect(os.environ['DB_CONNSTRING'])
    return conn

def get_sql_dict(q):
    """
    Takes a SELECT query and returns a dict for its cols/rows
    """
    cur = db_conn().cursor()
    cur.execute(q)

    data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    return data

@app.route("/")
def hello():
    return "Hello, Friends!\n"

@app.route("/users", methods=['GET'])
def get_users():
    page = request.args.get('page', default=1, type=int)
    page_size = 50

    offset = (page - 1) * page_size

    sql_q = f"SELECT * FROM users ORDER BY id LIMIT {page_size} OFFSET {offset}"

    return jsonify(get_sql_dict(sql_q))

@app.route("/user/<user_id>", methods=['GET'])
def get_user_by_id(user_id):

    sql_q = f"SELECT * FROM users WHERE id={user_id}"

    return jsonify(get_sql_dict(sql_q))

@app.route("/user/<user_id>/addresses")
def get_addresses_by_user_id(user_id):

    sql_q = f"SELECT * FROM addresses where user_id={user_id}"

    return jsonify(get_sql_dict(sql_q))

@app.route("/user/<user_id>/orders")
def get_orders_by_user_id(user_id):

    sql_q = f"SELECT * FROM orders where user_id={user_id}"

    return jsonify(get_sql_dict(sql_q))

@app.route("/address/<address_id>", methods=['GET'])
def get_addresses_by_id(address_id):

    sql_q = f"SELECT * FROM addresses WHERE id={address_id}"

    return jsonify(get_sql_dict(sql_q))

@app.route("/orders/<order_id>", methods=['GET'])
def get_order_by_id(order_id):

    sql_q = f"SELECT * FROM orders WHERE id={order_id}"

    return jsonify(get_sql_dict(sql_q))

@app.route("/products", methods=['GET'])
def get_products():

    sql_q = f"SELECT * FROM products ORDER BY id"

    return jsonify(get_sql_dict(sql_q))

@app.route("/product/<product_id>", methods=['GET'])
def get_product_by_id(product_id):

    sql_q = f"SELECT * FROM products WHERE id={product_id}"

    return jsonify(get_sql_dict(sql_q))


