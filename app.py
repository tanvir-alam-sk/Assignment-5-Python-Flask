from flask import Flask
from flasgger import Swagger
from controller.user_controller import home, register, login, get_profile, update_profile

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/", methods=["GET"])
def index():
    """
    Home Page
    ---
    tags:
      - Welcome
    responses:
      200:
        description: Returns a welcome message
        examples:
          text/plain: "Welcome to User"
    """
    return home()


@app.route('/register', methods=['POST'])
def register_user():
    """
    User Registration
    ---
    tags:
      - User Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Desired username
              example: johndoe
            email:
              type: string
              description: User's email address
              example: johndoe@example.com
            password:
              type: string
              description: User's password
              example: "password123"
    responses:
      201:
        description: User registered successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User registered successfully"
      400:
        description: Input validation error or duplicate username/email
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Username, Email and password are required"
    """
    return register()


@app.route("/login", methods=["POST"])
def login_user():
    """
    User Login
    ---
    tags:
      - User Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: User's email address
              example: johndoe@example.com
            password:
              type: string
              description: User's password
              example: password123
    responses:
      201:
        description: Login successful
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User logined successfully"
      400:
        description: Login failed (e.g., missing credentials or incorrect login details)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Email and password are required"
            message:
              type: string
              example: "Email or Password is not correct"
    """
    return login()


@app.route('/profile', methods=['GET'])
def view_profile():
    """
    Get User Profile
    ---
    tags:
      - User Management
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: JWT token for user authentication
        example: "Bearer <your_token>"
    responses:
      200:
        description: User profile retrieved successfully
        schema:
          type: object
          properties:
            username:
              type: string
              example: johndoe
            email:
              type: string
              example: johndoe@example.com
            password:
              type: string
              example: password123
            role:
              type: string
              example: user
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User not found"
      401:
        description: Unauthorized access
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid or expired token"
    """
    return get_profile()


@app.route('/profile', methods=['PATCH'])
def edit_profile():
    """
    Update User Profile
    ---
    tags:
      - User Management
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
            email:
              type: string
              description: The user's email (must match the logged-in user)
              example: johndoe@example.com
            username:
              type: string
              description: Updated username
              example: john_updated
            password:
              type: string
              description: Updated password
              example: newpassword123
            role:
              type: string
              description: Updated role
              example: admin
    responses:
      201:
        description: User information updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User Information Update successfully"
      403:
        description: Forbidden access (email mismatch)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Forbidden Access"
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User not found"
      400:
        description: Bad request (missing or invalid data)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Bad request"
    """
    return update_profile()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
