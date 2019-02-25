from app.database import db

todo_category_xref = \
    db.Table('todo_category_xref',
             db.Model.metadata,
             db.Column('todo_id', db.Integer, db.ForeignKey('todo.id')),
             db.Column('category_id', db.Integer, db.ForeignKey('category.id')))

todo_tag_xref = \
    db.Table('todo_tag_xref',
             db.Model.metadata,
             db.Column('todo_id', db.Integer, db.ForeignKey('todo.id')),
             db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))
