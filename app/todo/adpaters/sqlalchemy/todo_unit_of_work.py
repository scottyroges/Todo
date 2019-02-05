from app.server import db
from app.todo.adpaters.sqlalchemy.habit_repository import HabitRepository
from app.todo.domains.todo import Todo
from app.todo.domains.todo_type import TodoType


class SqlAlchemyTodoUnitOfWork:
    def __enter__(self):
        self.session = db.session
        self.habit_repo = HabitRepository(db.session)
        return self

    def __exit__(self, type, value, traceback):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def add(self, todo: Todo):
        if todo.todo_type == TodoType.HABIT:
            self.habit_repo.add(todo)
