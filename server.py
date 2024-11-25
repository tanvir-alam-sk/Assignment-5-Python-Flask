from flask import Flask
from flasgger import Swagger
from controller.destination_controller import get_all_destinations, add_destination, delete_destination

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/", methods=["GET"])
def home():
    """
    Home Page
    ---
    tags:
      - General
    responses:
      200:
        description: Welcome message
        schema:
          type: string
          example: "Welcome destination"
    """
    return "Welcome to the destination API"

@app.route("/destination", methods=["GET"])
def get_destination():
    """
    Retrieve Destination Information
    ---
    tags:
      - Destination
    responses:
      200:
        description: Successfully retrieved the destination data
        schema:
          type: object
          properties:
            Id:
              type: integer
              example: 99997
            Name:
              type: string
              example: "Grand Canyon"
            Description:
              type: string
              example: "A massive natural wonder in the USA, renowned for its stunning landscapes, hiking trails, and geological formations."
            Location:
              type: string
              example: "USA"
      500:
        description: Internal Server Error (e.g., file not found or unreadable)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Unable to load destination data"
    """
    return get_all_destinations()

@app.route("/destination", methods=["POST"])
def add_new_destination():
    """
    Add a new destination
    ---
    tags:
      - Destination
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: JWT token for user authentication
        example: "Bearer <your_token>"
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            Id:
              type: integer
              description: Unique identifier for the destination
              example: 99997
            Name:
              type: string
              description: Name of the destination
              example: Grand Canyon
            Description:
              type: string
              description: Detailed description of the destination
              example: "A massive natural wonder in the USA, renowned for its stunning landscapes, hiking trails, and geological formations."
            Location:
              type: string
              description: Geographical location of the destination
              example: "USA"
    responses:
      201:
        description: Destination added successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Destination Add successfully"
      400:
        description: Bad request (missing or invalid data)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Id, Location, Description and Location are required"
      401:
        description: Unauthorized access (user not found or not admin)
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Unauthorized Access"
      403:
        description: Forbidden access (only admins can add destinations)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Forbidden Access"
      409:
        description: Conflict (duplicate Id)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Id already taken please provide unique id"
    """
    return add_destination()

@app.route("/destination/<id>", methods=["DELETE"])
def remove_destination(id):
    """
    Delete a destination
    ---
    tags:
      - Destination
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: JWT token for user authentication
        example: "Bearer <your_token>"
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the destination to delete
        example: 99997
    responses:
      200:
        description: Destination deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Destination deleted successfully"
      400:
        description: Bad request (invalid or missing ID)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid ID provided"
      401:
        description: Unauthorized access (user not found or not admin)
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Unauthorized Access"
      403:
        description: Forbidden access (only admins can delete destinations)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Forbidden Access"
      404:
        description: Not found (destination does not exist)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Destination not found"
    """
    return delete_destination(id)



if __name__== "__main__":
    app.run(debug=True,port=5000)