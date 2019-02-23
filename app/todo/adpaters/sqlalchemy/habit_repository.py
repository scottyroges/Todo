from app.todo.adpaters.sqlalchemy.todo_repository import TodoRepository
from app.todo.domains.habit.habit import Habit as DomainHabit
from app.todo.transformers.habit_transformer import HabitTransformer


class HabitRepository(TodoRepository):
    def add(self, habit: DomainHabit) -> None:
        habit_record = HabitTransformer.to_record(habit)
        print(habit_record.__dict__)
        self._session.add(habit_record)
        self._session.commit()
        return habit
