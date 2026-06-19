#  Advanced Todo Management API

A secure RESTful API built using **Flask**, **SQLite**, **SQLAlchemy**, and **JWT Authentication**. The application allows users to register, log in, and manage their personal tasks with full CRUD functionality.

---

##  Features

### Authentication

* User Registration
* User Login
* JWT-based Authentication
* Protected User Profile Endpoint
* Password Hashing using Werkzeug

###  Task Management

* Create a Task
* View All Tasks
* View a Single Task
* Update Task Details
* Delete a Task
* User-specific task management

###  Additional Features

* SQLite database integration
* Logging and exception handling
* Modular architecture using Flask Blueprints
* JSON-based REST API

---

##  Tech Stack

* Python 
* Flask 
* Flask-SQLAlchemy
* Flask-JWT-Extended
* SQLite 
* Werkzeug Security
* Flask-Migrate
* Python Logging

---

##  Project Structure

```text
todo_adv/
│
├── migrations/
├── logs/
├── instance/
│   └── todo.db
│
├── __init__.py
├── app.py
├── config.py
├── models.py
├── services.py
├── routes.py
├── exceptions.py
├── create_db.py
├── requirements.txt
└── README.md
```

---

##  Database Schema

### User Table

| Field    | Type    | Description          |
| -------- | ------- | -------------------- |
| id       | INTEGER | Primary Key          |
| username | TEXT    | User's username      |
| email    | TEXT    | Unique email address |
| password | TEXT    | Hashed password      |

---

### Task Table

| Field       | Type    | Description                     |
| ----------- | ------- | ------------------------------- |
| id          | INTEGER | Primary Key                     |
| title       | TEXT    | Task title                      |
| description | TEXT    | Task description                |
| status      | TEXT    | Task status (Pending/Completed) |
| user_id     | INTEGER | Foreign Key referencing User    |

---

##  Authentication Endpoints

### Register User

**Endpoint**

```http
POST /register
```

**Request Body**

```json
{
  "username": "adithya",
  "email": "adithya@example.com",
  "password": "mypassword123"
}
```

**Response**

```json
{
  "message": "User Registered Successfully"
}
```

Status Code: `201 Created`

---

### Login User

**Endpoint**

```http
POST /login
```

**Request Body**

```json
{
  "email": "adithya@example.com",
  "password": "mypassword123"
}
```

**Response**

```json
{
  "access_token": "<jwt-token>"
}
```

Status Code: `200 OK`

---

### Get User Profile

**Endpoint**

```http
GET /profile
```

**Headers**

```text
Authorization: Bearer <jwt-token>
```

**Response**

```json
{
  "id": 1,
  "username": "adithya",
  "email": "adithya@example.com"
}
```

---

##  Task Endpoints

### Get All Tasks

```http
GET /tasks/
```

Returns all tasks belonging to the authenticated user.

---

### Get Single Task

```http
GET /tasks/<id>
```

Returns details of a specific task.

---

### Create Task

```http
POST /tasks/
```

**Request Body**

```json
{
  "title": "Complete Flask Project",
  "description": "Finish Todo API implementation"
}
```

**Response**

```json
{
  "id": 1,
  "title": "Complete Flask Project",
  "description": "Finish Todo API implementation",
  "status": "Pending"
}
```

Status Code: `201 Created`

---

### Update Task

```http
PUT /tasks/<id>
```

**Request Body**

```json
{
  "title": "Complete Flask Project",
  "description": "Add JWT Authentication",
  "status": "Completed"
}
```

---

### Delete Task

```http
DELETE /tasks/<id>
```

**Response**

```json
{
  "message": "Task Deleted Successfully"
}
```

---

##  Protected Routes

The following routes require a valid JWT token:

* `GET /profile`
* `GET /tasks/`
* `GET /tasks/<id>`
* `POST /tasks/`
* `PUT /tasks/<id>`
* `DELETE /tasks/<id>`

Include the token in the request header:

```text
Authorization: Bearer <jwt-token>
```

---

## Installation and Setup

### Clone the Repository

```bash
git clone https://github.com/your-username/advanced-todo-api.git
cd advanced-todo-api
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Database

```bash
python create_db.py
```

### Run Migrations

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Run the Application

```bash
python app.py
```

The server will start at:

```text
http://127.0.0.1:5000/
```

---

##  Testing

You can test the API using:

* Postman
* Thunder Client
* curl

Recommended workflow:

1. Register a user
2. Login and obtain JWT token
3. Add `Authorization: Bearer <token>` header
4. Access protected task endpoints

---


##  Author
Adthya .k.s

Built using Flask to practice REST API development, authentication, JWT implementation, SQLAlchemy ORM, database migrations, and secure user-specific task management.
