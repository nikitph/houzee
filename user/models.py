from bson import json_util
from extensions import db
from flask.ext.security import UserMixin, RoleMixin
import datetime

from mongoengine import QuerySet


class CustomQuerySet(QuerySet):
    def map_reduce(self, map_f, reduce_f, output, finalize_f=None, limit=None, scope=None):
        pass

    def to_json(self):
        return "[%s]" % (",".join([doc.to_json() for doc in self]))


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

    def __unicode__(self):
        return '%s' % self.name


class Notification(db.EmbeddedDocument):
    subject = db.StringField(max_length=1000)
    url = db.StringField(max_length=1500)
    message = db.StringField(default='placeholder', max_length=1500)
    read = db.BooleanField(default=False)

    # def __str__(self):
    #     return self.subject
    #
    # __rpr__ = __str__

    meta = {'queryset_class': CustomQuerySet}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo()
        return json_util.dumps(data, *args, **kwargs)


class User(UserMixin, db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    email = db.StringField(required=True, max_length=80, help_text='email')
    username = db.StringField(max_length=255, required=False)
    password = db.StringField(required=True, default='378965')
    active = db.BooleanField(default=True)
    first_name = db.StringField(required=True, max_length=100, help_text='account_box')
    last_name = db.StringField(required=True, max_length=100, help_text='perm_identity')
    image = db.StringField(required=False, max_length=200,
                           default='static/img/256px-Weiser_State_Forest_Walking_Path.jpg')
    phone = db.StringField(required=True, max_length=20, help_text='phone')
    address = db.StringField(max_length=255, required=False, default='')
    building = db.StringField(max_length=255, required=False, default='')
    buildingid = db.StringField(max_length=255, required=False, default='')
    notif = db.ListField(db.EmbeddedDocumentField(Notification))
    roles = db.ListField(db.ReferenceField(Role), default=[])
    # email confirmation
    confirmed_at = db.DateTimeField()
    # tracking
    last_login_at = db.DateTimeField()
    current_login_at = db.DateTimeField()
    last_login_ip = db.StringField()
    current_login_ip = db.StringField()
    login_count = db.IntField()

    def __unicode__(self):
        return '%s' % self.id

    def __repr__(self):
        return "%s %s %s" % (self.username, self.id, self.email)

    def get_id(self):
        return unicode(self.id)

    def get_building(self):
        return unicode(self.building)

    def is_manager(self):
        return self.has_role('manager')

    def is_resident(self):
        return self.has_role('resident')

    def is_staff(self):
        return "staff" in self.roles

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'email', 'username'],
        'ordering': ['-created_at'],
        'queryset_class': CustomQuerySet
    }

    def to_json(self, *args, **kwargs):
        data = self.to_mongo()
        data['notific'] = self.notif.to_json()
        return json_util.dumps(data, *args, **kwargs)
