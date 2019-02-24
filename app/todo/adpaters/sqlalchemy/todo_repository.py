from app.model import Todo
from app.server import db
from app.todo.domains.todo_type import TodoType
from app.todo.transformers.habit_transformer import HabitTransformer


class TodoRepository:
    def __init__(self):
        self._session = db.session

    def read(self, todo_id):
        todo_record = (self._session.query(Todo)
                       .get(todo_id))
        if todo_record.todo_type == TodoType.HABIT:
            return HabitTransformer.from_record(todo_record)

    def update(self, todo):
        if todo.todo_type == TodoType.HABIT:
            todo_record = HabitTransformer.to_record(todo)
        self._session.merge(todo_record)
        self._session.commit()
        return todo
