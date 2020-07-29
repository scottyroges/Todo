import datetime

from app.database import db
from app.model import Category
from app.todo.transformers.category_transformer import CategoryTransformer


class CategoryRepository:
    def __init__(self):
        self._session = db.session

    def add(self, category):
        category_record = CategoryTransformer.to_record(category)
        category_record.created_date = datetime.datetime.now()
        
        self._session.add(category_record)
        self._session.commit()

        return CategoryTransformer.from_record(category_record)

    def read_all(self, user_id):
        category_records = self._session.query(Category).filter_by(user_id=user_id).all()
        return [CategoryTransformer.from_record(category_record)
                for category_record in category_records]
