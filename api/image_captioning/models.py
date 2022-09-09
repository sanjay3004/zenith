import uuid

from sqlalchemy import Column, String, DateTime, Integer, Boolean, Enum, inspect, ForeignKey, VARCHAR, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property

from app import db
from app.models import BaseModel

class Post(BaseModel):
    __tablename__ = 'post'
    # __serialize_attributes__ = (
    #     'id', 'type', 'title', 'visibility', "user_id", "group_id", "meta_data", "location",
    #     "description", "expire_on")
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(Enum('regular', 'sports_activity', 'betting', 'repost','activity','betting_result','watch_activity','record_activity', name='post_type'))
    title = Column(VARCHAR(100))
    visibility = Column(Enum('admin','all', 'friends', 'private', 'custom', 'group', 'followers', name='visibility_type'))
    # group_id = Column(UUID(as_uuid=True) , default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), default=uuid.uuid4)
    group_id = Column(UUID(as_uuid=True), ForeignKey('user_group.id'), default=None)
    meta_data = Column(JSON)
    location = Column(JSON)
    description = Column(Text())
    expire_on = Column(DateTime)
    is_tag = Column(Boolean)
    promotion = Column(Boolean,default=False)
    share_link = Column(VARCHAR(255))
    status = Column(Enum('active', 'inactive', 'invited', name='status_type'),default='active')