"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# Ensure that the database is created inside the application context
with app.app_context():
    db.create_all()

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/api/cupcakes', methods=['GET'])
def list_cupcakes():
    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]
    print(serialized)  # Debugging: print the serialized data to verify image URLs
    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["GET"])
def get_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Create new cupcake"""
    # Ensure the request contains JSON data
    if not request.is_json:
        return jsonify(error="Invalid request: Content-Type must be application/json"), 400

    data = request.json

    # Validate the required fields
    flavor = data.get('flavor')
    size = data.get('size')
    rating = data.get('rating')
    
    if not flavor or not size or not rating:
        return jsonify(error="Missing required fields: flavor, size, and rating are required"), 400
    
    image = data.get('image') or None  # Handle optional image field
    
    # Create and save the cupcake
    cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image=image
    )

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize()), 201



@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update an existing cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json

    # UPDATE CUPCAKE ATTRIBUTES
    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize()) 


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete existing cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

@app.route('/cupcakes/<int:cupcake_id>')
def cupcake_details(cupcake_id):
    """Show the details page for a specific cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return render_template('cupcake_details.html', cupcake=cupcake)
