from models import (
    db,
    Task
)


def create_task(
    title,
    description,
    user_id
):

    task = Task(
        title=title,
        description=description,
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return task


def get_tasks(user_id):

    return Task.query.filter_by(
        user_id=user_id
    ).all()


def get_task(task_id):

    return Task.query.get(task_id)


def update_task(
    task,
    title,
    description,
    status
):

    task.title = title
    task.description = description
    task.status = status

    db.session.commit()

    return task


def delete_task(task):

    db.session.delete(task)

    db.session.commit()