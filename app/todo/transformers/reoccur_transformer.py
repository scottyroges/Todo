from app.model import (
    Action as ActionRecord,
    Category as CategoryRecord,
    Reoccur as ReoccurRecord,
    Tag as TagRecord
)
from app.todo.domains.action import Action as DomainAction
from app.todo.domains.reoccur.reoccur import Reoccur as DomainReoccur
from app.todo.domains.category import Category as DomainCategory
from app.todo.domains.reoccur.reoccur_repeat import ReoccurRepeat, ReoccurRepeatType
from app.todo.domains.tag import Tag as DomainTag
from app.todo.domains.todo_owner import TodoOwner


class ReoccurTransformer:
    @classmethod
    def to_record(cls, reoccur: DomainReoccur):
        repeat = {
            "repeatType": reoccur.repeat.repeat_type.name,
            "when": reoccur.repeat.when
        }

        category = CategoryRecord(
            id=reoccur.category.category_id,
            name=reoccur.category.name,
            color=reoccur.category.color
        )

        tags = [TagRecord(id=tag.tag_id,
                          name=tag.name)
                for tag in reoccur.tags]

        actions = [ActionRecord(id=action.action_id,
                                action_date=action.action_date,
                                points=action.points)
                   for action in reoccur.actions]

        return ReoccurRecord(todo_id=reoccur.todo_id,
                             todo_owner_id=reoccur.todo_owner.owner_id,
                             name=reoccur.name,
                             description=reoccur.description,
                             todo_type=reoccur.todo_type,
                             completion_points=reoccur.completion_points,
                             repeat=repeat,
                             required=reoccur.required,
                             category=category,
                             tags=tags,
                             actions=actions,
                             created_date=reoccur.created_date,
                             modified_date=reoccur.modified_date)

    @classmethod
    def from_record(cls, reoccur_record: ReoccurRecord):
        todo_owner = TodoOwner(owner_id=reoccur_record.todo_owner_id)
        repeat = ReoccurRepeat(repeat_type=ReoccurRepeatType[reoccur_record.repeat.get("repeatType")],
                               when=reoccur_record.repeat.get("when"))
        
        category = DomainCategory(category_id=reoccur_record.category.id,
                                  name=reoccur_record.category.name,
                                  color=reoccur_record.category.color)

        tags = [DomainTag(tag_id=tag.id,
                          name=tag.name)
                for tag in reoccur_record.tags]

        actions = [DomainAction(action_id=action.id,
                                action_date=action.action_date,
                                points=action.points)
                   for action in reoccur_record.actions]
        return DomainReoccur(todo_id=reoccur_record.todo_id,
                             todo_owner=todo_owner,
                             name=reoccur_record.name,
                             description=reoccur_record.description,
                             completion_points=reoccur_record.completion_points,
                             repeat=repeat,
                             required=reoccur_record.required,
                             category=category,
                             tags=tags,
                             actions=actions,
                             created_date=reoccur_record.created_date,
                             modified_date=reoccur_record.modified_date)
