from flask import Flask, render_template, request, redirect, jsonify
import requests

app = Flask(__name__)

# Define the base URL of your Flask-SQLAlchemy backend
base_url = ''  


@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to show form to add a new item
@app.route('/add', methods=['GET'])
def add_item_form():
    return render_template('add_item.html')

# Endpoint to submit new item data to the application tier
@app.route('/addItem', methods=['POST'])
def add_item():
    item_data = {
        'name': request.form['name'],
        'quantity': request.form['quantity']
    }
    response = requests.post(f'{base_url}/addItem', json=item_data)
    return redirect('/items')

# Endpoint to view all items
@app.route('/items', methods=['GET'])
def view_items():
    response = requests.get(f'{base_url}/items')
    items = response.json()
    return render_template('view_items.html', items=items)

@app.route('/deleteItem/<int:id>', methods=['POST'])
def delete_item(id):
    response = requests.delete(f'{base_url}/deleteItem/{id}')
    return redirect('/items')

if __name__ == "__main__":
    app.run(debug=True, port=5000,host='0.0.0.0')
