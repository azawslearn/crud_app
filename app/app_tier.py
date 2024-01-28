from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import config 

app = Flask(__name__)

# Construct the SQLAlchemy Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

# Define the inventory model
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity
        }

# Manually create tables using app_context
with app.app_context():
    db.create_all()

# Route to add a new item
@app.route('/addItem', methods=['POST'])
def add_item():
    try:
        name = request.json['name']
        quantity = request.json['quantity']
        new_item = Inventory(name, quantity)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Item added successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Route to get all items
@app.route('/items', methods=['GET'])
def get_items():
    try:
        items = Inventory.query.all()
        return jsonify([item.serialize() for item in items])
    except Exception as e:
        return jsonify({'error': str(e)})

# Route to delete an item
@app.route('/deleteItem/<int:id>', methods=['DELETE'])
def delete_item(id):
    try:
        item = Inventory.query.get(id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': 'Item deleted successfully!'})
        else:
            return jsonify({'message': 'Item not found'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
