from app.todo.todo_repository_factory import TodoRepositoryFactory


def get_todos(user_id, only_shows=False):
    repo = TodoRepositoryFactory.create()
    todos = repo.read_all(user_id)
    if only_shows:
        todos = list(filter(lambda x: x.should_show is True, todos))
    return todos
