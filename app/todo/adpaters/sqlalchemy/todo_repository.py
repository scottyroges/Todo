from app.model import Todo
from app.database import db
from app.todo.domains.todo_type import TodoType
from app.todo.transformers.habit_transformer import HabitTransformer
from app.todo.transformers.reoccur_transformer import ReoccurTransformer
from app.todo.transformers.task_transformer import TaskTransformer
import logging


class TodoRepository:
    def __init__(self):
        self._session = db.session

    def add(self, todo):
        todo_record = self._get_transformer(todo.todo_type).to_record(todo)

        self._session.add(todo_record)
        self._session.commit()

        return self._get_transformer(todo.todo_type).from_record(todo_record)

    def _read(self, todo_id):
        todo_record = (self._session.query(Todo).get(todo_id))
        if todo_record is None:
            return None
        return todo_record

    def read(self, todo_id):
        todo_record = self._read(todo_id)

        if todo_record is None:
            return None

        return self._get_transformer(todo_record.todo_type).from_record(todo_record)

    def read_all(self, user_id):
        todo_records = self._session.query(Todo).filter_by(todo_owner_id=user_id).all()
        return [self._get_transformer(todo_record.todo_type).from_record(todo_record)
                for todo_record in todo_records]

    def update(self, todo):
        print("updating todo")
        todo_record = self._get_transformer(todo.todo_type).to_record(todo)

        previous_todo_record = self._read(todo_record.todo_id)

        if previous_todo_record.todo_type != todo_record.todo_type:
            logging.info("trying to update todo type")
            self._session.delete(previous_todo_record)

        todo_record = self._session.merge(todo_record)
        self._session.commit()

        self._session.expire(todo_record, ['category'])
        return self._get_transformer(todo.todo_type).from_record(todo_record)

    def _get_transformer(self, todo_type):
        if todo_type == TodoType.HABIT:
            return HabitTransformer
        elif todo_type == TodoType.REOCCUR:
            return ReoccurTransformer
        elif todo_type == TodoType.TASK:
            return TaskTransformer
