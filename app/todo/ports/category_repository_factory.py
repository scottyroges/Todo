from app.todo.adpaters.sqlalchemy.category_repository import CategoryRepository


class CategoryRepositoryFactory:
    @classmethod
    def create(cls):
        return CategoryRepository()
