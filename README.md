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
   git clone https://github.com/yourusername/task-manager-flask.git
   ```

2. Navigate to the project directory:

   ```bash
   cd task-manager-flask
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
   python app.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

## Project Structure

- `app.py`: The main application file.
- `templates/`: Directory containing HTML templates.
  - `index.html`: Template for displaying tasks.
  - `update.html`: Template for updating tasks.
- `task_db.db`: SQLite database file.

## Models

### Todo

- `id`: Integer, primary key.
- `content`: String, task content.
- `completed`: Integer, task completion status (default is 0).
- `date_created`: DateTime, task creation date (default is current UTC time).

## Routes

- `/`: Main page to view and add tasks.
- `/delete/<int:id>`: Route to delete a task by its ID.
- `/update/<int:id>`: Route to update a task by its ID.

## License

This project is licensed under the MIT License.
