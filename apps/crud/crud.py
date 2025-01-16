import sqlite3
from flask import Flask, request, jsonify, render_template, Blueprint
from models import query_db

crud_bp = Blueprint('crud', __name__, template_folder='templates', static_folder='static')

# Routes
@crud_bp.route('/')
def home():
    return render_template('index.html')

# Create
@crud_bp.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    name = data['name']
    description = data.get('description')
    query_db('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
    return jsonify({"name": name, "description": description}), 201

# Read All
@crud_bp.route('/items', methods=['GET'])
def get_items():
    items = query_db('SELECT * FROM items')
    return jsonify([{ "id": row[0], "name": row[1], "description": row[2] } for row in items])

# Read One
@crud_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = query_db('SELECT * FROM items WHERE id = ?', (item_id,), one=True)
    if item:
        return jsonify({"id": item[0], "name": item[1], "description": item[2]})
    return jsonify({"error": "Item not found"}), 404

# Update
@crud_bp.route('/items/<int:item_id>', methods=['PUT'])
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
@crud_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = query_db('SELECT * FROM items WHERE id = ?', (item_id,), one=True)
    if item:
        query_db('DELETE FROM items WHERE id = ?', (item_id,))
        return '', 204
    return jsonify({"error": "Item not found"}), 404