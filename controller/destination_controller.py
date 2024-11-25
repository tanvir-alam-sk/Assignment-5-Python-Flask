from flask import jsonify, request
from model.destination import read_destination, write_destination
from utility.jwt import verify_token
from model.user import read_users

def get_all_destinations():
    try:
        destination = read_destination()
        return jsonify(destination), 200
    except Exception:
        return jsonify({"error": "Unable to load destination data"}), 500

def add_destination():
    jwt_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    logined_user_email = verify_token(jwt_token)

    if not logined_user_email:
        return jsonify({"message": "Unauthorized Access"}), 401

    users = read_users()
    for user in users:
        if user['email'] == logined_user_email:
            if user['role'] != "admin":
                return jsonify({"error": "Forbidden Access"}), 403
            break
    else:
        return jsonify({"message": "Unauthorized Access"}), 401

    destinations = read_destination()
    data = request.get_json()

    required_fields = ['Id', 'Name', 'Description', 'Location']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Id, Name, Description, and Location are required"}), 400

    if any(destination['Id'] == data['Id'] for destination in destinations):
        return jsonify({"error": "Id already taken, please provide a unique id"}), 409

    destinations.append(data)
    write_destination(destinations)

    return jsonify({"message": "Destination added successfully"}), 201

def delete_destination(id):
    jwt_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    logined_user_email = verify_token(jwt_token)

    if not logined_user_email:
        return jsonify({"message": "Unauthorized Access"}), 401

    users = read_users()
    for user in users:
        if user['email'] == logined_user_email:
            if user['role'] != "admin":
                return jsonify({"error": "Forbidden Access"}), 403
            break
    else:
        return jsonify({"message": "Unauthorized Access"}), 401

    destinations = read_destination()

    destination_to_delete = next((dest for dest in destinations if dest['Id'] == int(id)), None)
    if not destination_to_delete:
        return jsonify({"error": "Destination not found"}), 404

    destinations.remove(destination_to_delete)
    write_destination(destinations)

    return jsonify({"message": "Destination deleted successfully"}), 200
