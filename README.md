# Task Master Using Python Flask

These are Python functions handling HTTP requests. Controllers are defined for specific tasks like registering users, logging in, managing user profiles, and CRUD operations on destinations only for Admin. Ensure that they respond correctly with appropriate status codes (e.g., 200, 401, 404).

## Features

#For User

- Add new tasks
- Delete existing tasks
- Update tasks
- View all tasks

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/TanvirAlamSk/Assignment-5 flask-assignment
   ```

2. Navigate to the project directory:

   ```bash
   cd flask-assignment
   ```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

5. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:

   ```bash
   -python server.py (5000 port)
   -python app.py (5000 port)

   ```

2. Open your web browser and go to `http://127.0.0.1:5000/ & http://127.0.0.1:5001/`.
2. Open your web browser # with Swagger and go to `http://127.0.0.1:5000/apidocs & http://127.0.0.1:5001/apidocs`.


## Project Structure

- `app.py`: The main user regintration, login and get loged in user profie file.
- `serer.py`: The main add,remove,and updaate destination by only Admin file.
- `templates/`: Directory containing HTML templates.
  - `index.html`: Template for displaying tasks.
  - `update.html`: Template for updating tasks.
- `db/destinations.py`: Save destination as a database file.
- `db/users.py`: Save users as a database file.

## Routes

- `/`: Main page to view and add tasks.
- `/register`: Reagister New User.
- `/login`: Login user.
- `/profile`: Get loded in User Profile.

- `/destination`: Get All Destination.
- `/destination/<id>`: Post a Destination.
- `/destination/<id>`: Delete a Destination.

## Test Coverage

Coverage tools (like coverage.py) measure how much of your code is executed during tests.

-Run: ``` coverage report -m ```

## License

This project is licensed under the MIT License.
