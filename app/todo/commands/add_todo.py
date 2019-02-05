from app.todo.adpaters.sqlalchemy.todo_unit_of_work import SqlAlchemyTodoUnitOfWork
from app.todo.domains.todo_owner import TodoOwner
from app.todo.todo_factory import TodoFactory


class AddTodo:
    uow = SqlAlchemyTodoUnitOfWork

    def execute(self, todo_data, todo_type):
        todo = TodoFactory.create_todo(todo_data, todo_type)

        todo_owner = TodoOwner(owner_id=todo_data.get("todo_owner_id"))
        todo.todo_owner = todo_owner
        with self.uow() as tx:
            tx.add(todo)
            tx.commit()
        return todo
