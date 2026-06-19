from flask import (
    request,
    jsonify,
    Blueprint
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from services import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from models import (
    db,
    User,
    Task
)

import logging
from exceptions import TaskNotFoundError

task_bp = Blueprint(
    "task",
    __name__,
    url_prefix="/tasks"
)

@task_bp.route("/", methods=["GET"])
@jwt_required()
def all_tasks():

    try:
        user_id = get_jwt_identity()

        tasks = get_tasks(user_id)

        return jsonify(
            [task.to_dict() for task in tasks]
        )

    except Exception as e:

        logging.error(
            f"Get Tasks Error: {str(e)}"
        )

        return jsonify({
            "error": "Failed to fetch tasks"
        }), 500


@task_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def single_task(id):
    try:
        task = get_task(id)
        if not task:
           raise TaskNotFoundError(
               f"Task{id} not found")

        return jsonify(task.to_dict())

    except Exception as e:

        logging.error(
            f"Get Task Error: {str(e)}"
        )

        return jsonify({
            "error": "Failed to fetch task"
        }), 500


@task_bp.route("/", methods=["POST"])
@jwt_required()
def add_task():

    try:

        user_id = get_jwt_identity()

        data = request.get_json()

        task = create_task(
            data["title"],
            data["description"],
            user_id
        )

        logging.info(
            f"Task Created: {task.title}"
        )

        return jsonify(
            task.to_dict()
        ), 201

    except Exception as e:

        logging.error(
            f"Create Task Error: {str(e)}"
        )

        return jsonify({
            "error": "Task Creation Failed"
        }), 500


@task_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def modify_task(id):

    try:

        task = get_task(id)

        if not task:
            return jsonify({
                "error": "Task Not Found"
            }), 404

        data = request.get_json()

        update_task(
            task,
            data["title"],
            data["description"],
            data["status"]
        )

        logging.info(
            f"Task Updated: {task.id}"
        )

        return jsonify(
            task.to_dict()
        )

    except Exception as e:

        logging.error(
            f"Update Task Error: {str(e)}"
        )

        return jsonify({
            "error": "Task Update Failed"
        }), 500


@task_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def remove_task(id):

    try:

        task = get_task(id)

        if not task:
            return jsonify({
                "error": "Task Not Found"
            }), 404

        delete_task(task)

        logging.info(
            f"Task Deleted: {id}"
        )

        return jsonify({
            "message": "Task Deleted Successfully"
        })

    except Exception as e:

        logging.error(
            f"Delete Task Error: {str(e)}"
        )

        return jsonify({
            "error": "Task Delete Failed"
        }), 500

api_bp = Blueprint(
    "api",
    __name__
)
@api_bp.route("/register", methods=["POST"])
def register():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data provided"
            }), 400

        if not data.get("username"):
            return jsonify({
                "error": "Username required"
            }), 400

        if not data.get("email"):
            return jsonify({
                "error": "Email required"
            }), 400

        if not data.get("password"):
            return jsonify({
                "error": "Password required"
            }), 400

        existing_user = User.query.filter_by(
            email=data["email"]
        ).first()

        if existing_user:
            return jsonify({
                "error": "Email already exists"
            }), 409

        hashed_password = generate_password_hash(
            data["password"]
        )

        user = User(
            username=data["username"],
            email=data["email"],
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        logging.info(
            f"User Registered: {user.email}"
        )

        return jsonify({
            "message": "User Registered Successfully"
        }), 201

    except Exception as e:

        logging.error(str(e))

        return jsonify({
            "error": "Registration Failed"
        }), 500
    
@api_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(
            email=data["email"]
        ).first()
        if not user:
            logging.warning(
                f"Invalid Login: {data['email']}"
            )

            return jsonify({
                "error": "Invalid Credentials"
            }), 401

        if not check_password_hash(
            user.password,
            data["password"]
        ):

            logging.warning(
                f"Wrong Password: {data['email']}"
            )

            return jsonify({
                "error": "Invalid Credentials"
            }), 401

        token = create_access_token(
            identity=str(user.id)
        )

        logging.info(
            f"User Logged In: {user.email}"
        )

        return jsonify({
            "access_token": token
        })

    except Exception as e:
        logging.error(str(e))
        return jsonify({
            "error": "Login Failed"
        }), 500
    
@api_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                "error": "User Not Found"
            }), 404

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })

    except Exception as e:
        logging.error(str(e))
        return jsonify({
            "error": "Profile Fetch Failed"
        }), 500