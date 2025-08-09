# user_client_view
user_client_view
1. Project Setup and Dependencies
You'll need a basic Django project with Django REST Framework (DRF) for building the APIs.

Prerequisites:

Python 3.8+
pip (Python package installer)
PostgreSQL or MySQL database server running
A code editor (VS Code, PyCharm, etc.)
Explanation:
User: We use Django's built-in User model. This is crucial for authentication and for linking created_by to the current user.
Client: Has a client_name and a created_by ForeignKey to the User who created it. created_at and updated_at fields are handled automatically.
Project:
client: A ForeignKey to the Client model. The related_name='projects' allows you to access Project objects from a Client instance (e.g., client.projects.all()).
users: A ManyToManyField to the User model, as a single project can be assigned to multiple users, and a single user can be assigned to multiple projects. related_name='projects' is used to access projects from a User instance.
created_by: A ForeignKey to the User who created the project.
Run Migrations:
Bash
python manage.py makemigrations
python manage.py migrate
Create a superuser: This will be your initial User for testing.
Bash
python manage.py createsuperuser
Run the development server:
Bash
python manage.py runserver

Example API Requests:

GET /api/clients/: List all clients.

POST /api/clients/: Create a new client.

Input: {"client_name": "New Company"}

GET /api/clients/1/: Retrieve client with ID 1, including its projects.

POST /api/clients/1/projects/: Create a new project for client with ID 1.

Input: {"project_name": "New Project", "users": [{"id": 1}]}

GET /api/projects/: Retrieve all projects assigned to the logged-in user.
