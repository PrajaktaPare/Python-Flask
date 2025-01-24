from flask import Blueprint, request, jsonify
from models.authors import AuthorsModel  # Import the AuthorsModel from your models

author_bp = Blueprint('authors', __name__)
authors_model = AuthorsModel()  # Initialize the model

# Create a new author
@author_bp.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    if 'username' not in data or 'email' not in data or 'password_hash' not in data or 'bio' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        author_id = authors_model.create_author(data['username'], data['email'], data['password_hash'], data['bio'])
        return jsonify({'message': 'Author created successfully', 'author_id': author_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get all authors
@author_bp.route('/authors', methods=['GET'])
def get_all_authors():
    try:
        authors = authors_model.fetch_all_authors()
        return jsonify(authors)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get a specific author by ID
@author_bp.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    try:
        author = authors_model.fetch_author_by_id(author_id)
        if not author:
            return jsonify({'error': 'Author not found'}), 404
        return jsonify(author)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update an author by ID
@author_bp.route('/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    data = request.get_json()
    if not authors_model.fetch_author_by_id(author_id):
        return jsonify({'error': 'Author not found'}), 404

    try:
        authors_model.update_author(
            author_id,
            data.get('username'),
            data.get('email'),
            data.get('password_hash'),
            data.get('bio'),
            data.get('is_verified', False),
            data.get('is_flagged', False),
            data.get('is_approved', False)
        )
        return jsonify({'message': 'Author updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete an author by ID
@author_bp.route('/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    if not authors_model.fetch_author_by_id(author_id):
        return jsonify({'error': 'Author not found'}), 404

    try:
        authors_model.delete_author(author_id)
        return jsonify({'message': 'Author deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
