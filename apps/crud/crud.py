import sqlite3
from flask import Flask, request, jsonify, render_template, Blueprint

DATABASE = 'instance/UserLog.db'
crud = Blueprint('crud', __name__, template_folder='templates', static_folder='static')

# Helper function to query the database
def query_db(query, args=(), one=False):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        rv = cursor.fetchall()
        conn.commit()
        return (rv[0] if rv else None) if one else rv

# Routes
@crud.route('/')  # Change this to use the blueprint's route
def crud_index():
    return render_template('index.html')

# Create
@crud.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    name = data['name']
    description = data.get('description')
    query_db('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
    return jsonify({"name": name, "description": description}), 201

# Read All
@crud.route('/items', methods=['GET'])
def get_items():
    items = query_db('SELECT * FROM items')
    return jsonify([{ "id": row[0], "name": row[1], "description": row[2] } for row in items])

# Read One
@crud.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = query_db('SELECT * FROM items WHERE id = ?', (item_id,), one=True)
    if item:
        return jsonify({"id": item[0], "name": item[1], "description": item[2]})
    return jsonify({"error": "Item not found"}), 404

# Update
@crud.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    item = query_db('SELECT * FROM items WHERE id = ?', (item_id,), one=True)
    if item:
        query_db('UPDATE items SET name = ?, description = ? WHERE id = ?', (name or item[1], description or item[2], item_id))
        return jsonify({"id": item_id, "name": name or item[1], "description": description or item[2]})
    return jsonify({"error": "Item not found"}), 404

# Delete
@crud.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = query_db('SELECT * FROM items WHERE id = ?', (item_id,), one=True)
    if item:
        query_db('DELETE FROM items WHERE id = ?', (item_id,))
        return '', 204
    return jsonify({"error": "Item not found"}), 404