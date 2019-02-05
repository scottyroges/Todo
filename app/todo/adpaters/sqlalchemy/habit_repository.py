from app.todo.domains.habit import Habit


class HabitRepository:
    def __init__(self, session):
        self._session = session

    def add(self, habit: Habit) -> None:
        self._session.add(habit)
