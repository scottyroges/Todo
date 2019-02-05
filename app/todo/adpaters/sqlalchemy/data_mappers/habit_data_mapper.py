import json

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String, Text,
    Enum,
    JSON,
    DateTime
)
from sqlalchemy.orm import mapper, composite

from app.database.sqlalchemy.sqlalchemy_data_mapper import SqlAlchemyDataMapper
from app.todo.domains.habit import Habit
from app.todo.domains.habit_buffer import HabitBuffer
from app.todo.domains.todo_owner import TodoOwner
from app.todo.domains.todo_type import TodoType


class HabitDataMapper(SqlAlchemyDataMapper):

    @classmethod
    def configure_mappings(cls, db):
        TodoOwner.__composite_values__ = lambda i: [i.owner_id]
        HabitBuffer.__composite_values__ = lambda i: (
            [json.dumps(
                {
                    "buffer_type": i.buffer_type,
                    "amount": i.amount
                }
            )])

        habit_table = Table('habit', db.metadata,
                            Column('todo_id', String(36), primary_key=True),
                            Column('todo_owner_id', String(36), nullable=False),
                            Column('name', String(255)),
                            Column('description', Text),
                            Column('todo_type', Enum(TodoType)),
                            Column('points_per', Integer),
                            Column('completion_points', Integer),
                            Column('frequency', Integer),
                            Column('period', JSON),
                            Column('buffer', JSON),
                            Column('created_date', DateTime),
                            Column('modified_date', DateTime))
        mapper(
            Habit,
            habit_table,
            properties={
                'todo_owner': composite(TodoOwner, habit_table.c.todo_owner_id),
                'buffer': composite(HabitBuffer, habit_table.c.buffer)
            },
        )
