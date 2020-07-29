from app.model import Category as CategoryRecord
from app.todo.domains.category import Category as DomainCategory


class CategoryTransformer:
    @classmethod
    def to_record(cls, category: DomainCategory):
        return CategoryRecord(
            id=category.category_id,
            user_id=category.user_id,
            name=category.name,
            color=category.color
        )

    @classmethod
    def from_record(cls, category_record: CategoryRecord):
        return DomainCategory(
            category_id=category_record.id,
            user_id=category_record.user_id,
            name=category_record.name,
            color=category_record.color
        )
