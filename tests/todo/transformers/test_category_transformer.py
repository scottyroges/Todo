from app.todo.domains.category import Category as DomainCategory
from app.model import Category as CategoryRecord
from app.todo.transformers.category_transformer import CategoryTransformer


def test_to_record():
    category = DomainCategory(
        category_id="123",
        user_id="abc",
        name="test",
        color="#FFF"
    )

    category_record = CategoryTransformer.to_record(category)

    assert category_record.id == category.category_id
    assert category_record.user_id == category.user_id
    assert category_record.name == category.name
    assert category_record.color == category.color


def test_from_record():
    category_record = CategoryRecord(
        id="123",
        user_id="abc",
        name="test",
        color="#FFF"
    )

    category = CategoryTransformer.from_record(category_record)

    assert category.category_id == category_record.id
    assert category.user_id == category_record.user_id
    assert category.name == category_record.name
    assert category.color == category_record.color
