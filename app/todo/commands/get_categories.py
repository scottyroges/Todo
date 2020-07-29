from app.todo.ports.category_repository_factory import CategoryRepositoryFactory


class GetCategories:
    def execute(self, user_id):
        repo = CategoryRepositoryFactory.create()
        return repo.read_all(user_id)
