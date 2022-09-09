from datetime import datetime

from flask_mongoengine import DynamicDocument
from mongoengine import ValidationError

from app import mongodb as db


# ToDo: On Update function, updated_at not updating.
class BaseModel(DynamicDocument):
    meta = {'allow_inheritance': True, 'abstract': True}
    created_on = db.DateTimeField(default=datetime.now())
    updated_on = db.DateTimeField(default=datetime.now())
    deleted_on = db.DateTimeField(default=None)
    created_by = db.StringField(default=None)
    updated_by = db.StringField(default=None)
    deleted_by = db.StringField(default=None)
    is_deleted = db.BooleanField(default=False)

    def save(self, user_name=None, *args, **kwargs):
        current_time = datetime.now()
        self.created_on = current_time
        self.updated_on = current_time
        self.created_by = user_name
        return super(BaseModel, self).save(*args, **kwargs)

    def delete(self, user_name=None, *args, **kwargs):
        current_time = datetime.now()
        self.is_deleted = True
        self.deleted_by = user_name
        self.deleted_on = current_time
        return super(BaseModel, self).save()

    def update(self, user_name=None, *args, **kwargs):
        current_time = datetime.now()
        self.updated_on = current_time
        self.updated_by = user_name
        super(BaseModel, self).update(**kwargs)
        return super(BaseModel, self).save(**kwargs)


def _not_empty(val):
    if not val:
        raise ValidationError('value can not be empty')
