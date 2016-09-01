import datetime

from bson import json_util
from mongoengine import EmbeddedDocumentField, ListField, Document, DynamicDocument, ReferenceField, QuerySet
from user.models import User
from extensions import db


class CustomQuerySet(QuerySet):
    def map_reduce(self, map_f, reduce_f, output, finalize_f=None, limit=None, scope=None):
        pass

    def to_json(self):
        return "[%s]" % (",".join([doc.to_json() for doc in self]))


class Township(db.Document):
    name = db.StringField(required=True, max_length=50, help_text='perm_identity')
    builder = db.StringField(required=True, max_length=50, help_text='build')
    address = db.StringField(required=True, help_text='location_on')
    city = db.StringField(required=True, max_length=50, help_text='location_city')
    state = db.StringField(required=True, max_length=50, help_text='location_searching')
    pincode = db.IntField(required=True, help_text='local_parking')
    phone = db.StringField(required=True, max_length=50, help_text='phone')
    website = db.StringField(required=True, max_length=50, help_text='web')
    email = db.StringField(required=True, max_length=50, help_text='email')

    def __str__(self):
        return self.name

    __rpr__ = __str__


class Building(db.Document):
    township = db.StringField(required=True, max_length=100, help_text='')
    user = db.StringField(required=True, max_length=50, help_text='')
    building_name = db.StringField(required=True, max_length=50, help_text='perm_identity')
    street_address = db.StringField(required=True, help_text='location_on')
    city = db.StringField(required=True, max_length=50, help_text='location_city')
    state = db.StringField(required=True, max_length=50, help_text='navigation')
    pincode = db.IntField(required=True, help_text='local_parking')
    phone = db.StringField(required=True, max_length=50, help_text='phone')
    website = db.StringField(required=True, max_length=50, help_text='website')
    email = db.StringField(required=True, max_length=50, help_text='email')


class Apartment(db.Document):
    apartment_name = db.StringField(required=True, max_length=100, help_text='domain')
    apartment_details = db.StringField(required=True, max_length=100, help_text='description')
    parking_spot = db.StringField(required=True, max_length=100, help_text='parking')
    building = db.StringField(required=True, max_length=50, help_text='')

    def __str__(self):
        return self.apartment_name

    __rpr__ = __str__


#
#
# class Subject(db.Document):
#     code = db.StringField(required=True, max_length=50, help_text='code')
#     subject_name = db.StringField(required=True, max_length=50, help_text='book')
#     books = db.StringField(required=True, max_length=50, help_text='library_books')
#     syllabus = db.StringField(required=True, max_length=50, help_text='content_paste')
#     total_theory_hours = db.IntField(required=True, help_text='hourglass_empty')
#     class_duration = db.IntField(required=True, help_text='hourglass_full')
#     description = db.StringField(required=True, help_text='description')
#     school = db.StringField(required=True, max_length=50, help_text='')
#
#     def __str__(self):
#         return self.subject_name
#
#     __rpr__ = __str__
#
#
# class Teacher(db.Document):
#     teacher_name = db.StringField(required=True, max_length=50, help_text='perm_identity')
#     gender = db.BooleanField(required=True)
#     street_address = db.StringField(required=True, help_text='location_on')
#     city = db.StringField(required=True, max_length=20, help_text='location_city')
#     state = db.StringField(required=True, max_length=20, help_text='navigation')
#     pincode = db.StringField(required=True, max_length=20, help_text='local_parking')
#     email = db.StringField(required=True, max_length=50, help_text='email')
#     phone = db.StringField(required=True, max_length=50, help_text='phone')
#     school = db.StringField(required=True, max_length=100, help_text='')
#     subjects = db.ListField(ReferenceField(Subject, required=True))
#
#     def __str__(self):
#         return self.teacher_name
#
#     __rpr__ = __str__
#
#
# class ClassRoom(db.Document):
#     school = db.StringField(required=True, max_length=50)
#     class_name = db.StringField(required=True, max_length=50, help_text='perm_identity')
#     class_teacher = db.ReferenceField(Teacher, required=True)
#     subjects = ListField(ReferenceField(Subject), required=True)
#     location = db.StringField(required=False, max_length=100, help_text='location_on')
#     description = db.StringField(required=False, help_text='description')
#
#     def __str__(self):
#         return self.class_name
#
#     __rpr__ = __str__
#
#     meta = {'queryset_class': CustomQuerySet}
#
#     def to_json(self, *args, **kwargs):
#         data = self.to_mongo()
#         data["class_teacher"] = self.class_teacher.teacher_name
#         return json_util.dumps(data, *args, **kwargs)


class Resident(User):
    building = db.StringField(required=True, max_length=100, help_text='')
    apartment = db.ReferenceField(Apartment, required=True, help_text='activateSlave(this);')
    date_of_birth = db.StringField(required=True, max_length=20, help_text='cake')
    related = db.DictField(required=False)
    image = db.StringField(required=False, max_length=200,
                           default='static/img/256px-Weiser_State_Forest_Walking_Path.jpg')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    __rpr__ = __str__

    meta = {'queryset_class': CustomQuerySet}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo()
        data["apartment"] = self.apartment.apartment_name
        return json_util.dumps(data, *args, **kwargs)


# class Parent(db.Document):
#     relationship = db.StringField(required=True, max_length=20, help_text='supervisor_account')
#     parent_name = db.StringField(required=True, max_length=20, help_text='perm_identity')
#     student_id = db.StringField(required=True, max_length=50, help_text='')
#     street_address = db.StringField(required=True, help_text='location_on')
#     city = db.StringField(required=True, max_length=20, help_text='location_city')
#     state = db.StringField(required=True, max_length=20, help_text='navigation')
#     pincode = db.StringField(required=True, max_length=20, help_text='local_parking')
#     annual_income = db.StringField(required=True, max_length=50, help_text='monetization_on')
#     occupation = db.StringField(required=True, max_length=50, help_text='work')
#     phone = db.StringField(required=True, max_length=20, help_text='phone')
#     email = db.StringField(required=True, max_length=20, help_text='email')
#
#     def save(self, *args, **kwargs):
#         super(Parent, self).save(*args, **kwargs)
#         stu = Student.objects(id=self.student_id).first()
#         keys = {str(self.id): 'parent'}
#         set_new = dict((("set__related__%s" % k, v) for k, v in keys.iteritems()))
#         stu.update(**set_new)
#
#
# class Scholarship(db.Document):
#     awarding_body = db.StringField(required=True, max_length=20, help_text='')
#     year = db.StringField(required=True, max_length=20, help_text='')
#     student_id = db.StringField(required=True, max_length=50, help_text='')
#     title_of_scholarship = db.StringField(required=True)
#
#     def save(self, *args, **kwargs):
#         super(Scholarship, self).save(*args, **kwargs)
#         stu = Student.objects(id=self.student_id).first()
#         keys = {str(self.id): 'scholarship'}
#         set_new = dict((("set__related__%s" % k, v) for k, v in keys.iteritems()))
#         stu.update(**set_new)
#
#
# class Award(db.Document):
#     awarding_body = db.StringField(required=True, max_length=20, help_text='')
#     year = db.StringField(required=True, max_length=20, help_text='')
#     student_id = db.StringField(required=True, max_length=50, help_text='')
#     title_of_award = db.StringField(required=True)
#
#     def save(self, *args, **kwargs):
#         super(Award, self).save(*args, **kwargs)
#         stu = Student.objects(id=self.student_id).first()
#         keys = {str(self.id): 'award'}
#         set_new = dict((("set__related__%s" % k, v) for k, v in keys.iteritems()))
#         stu.update(**set_new)


class Profile(db.Document):
    user = db.StringField(required=True, max_length=50, help_text='')
    phone = db.StringField(required=True, max_length=50, help_text='phone')
    address = db.StringField(required=True, max_length=50, help_text='location_on')
    email = db.StringField(required=True, max_length=50, help_text='email')
    photo = db.StringField(required=True, max_length=50, help_text='')


class Event(db.Document):
    building = db.StringField(required=True, max_length=50, help_text='')
    event_name = db.StringField(required=True, max_length=50, help_text='perm_identity')
    from_date = db.StringField(required=True, max_length=50, help_text='date_range')
    to_date = db.StringField(required=True, max_length=50, help_text='date_range')
    start_time = db.StringField(required=True, max_length=50, help_text='hourglass_full')
    end_time = db.StringField(required=True, max_length=50, help_text='hourglass_empty')
    location = db.StringField(required=True, max_length=50, help_text='location_on')
    # event_for = db.StringField(required=True, verbose_name='Event is for',
    #                            choices=(('1', "Everyone"), ('2', "Students"), ('3', "Faculty"), ('4', "Parents")))
    description = db.StringField(required=True, help_text='description')

    def __str__(self):
        return self.event_name

    __rpr__ = __str__


class BulkNotification(db.Document):
    building = db.StringField(required=True, max_length=50, help_text='')
    subject = db.StringField(required=True, max_length=200, help_text='mail_outline')
    body = db.StringField(required=True, verbose_name='Notification Message', help_text='subject')


class News(db.Document):
    building = db.StringField(required=True, max_length=50, help_text='')
    headline = db.StringField(required=True, max_length=200, help_text='mail_outline')
    details = db.StringField(required=True, help_text='subject')
    # creation_date = db.DateTimeField(default=datetime.datetime.now)
    #
    # def __str__(self):
    #     return self.headline
    #
    # __rpr__ = __str__
    #
    # meta = {'queryset_class': CustomQuerySet}
    #
    # def to_json(self, *args, **kwargs):
    #     data = self.to_mongo()
    #     data["creation_date"] = self.creation_date.isodate()
    #     return json_util.dumps(data, *args, **kwargs)


class Item(db.Document):
    building = db.StringField(required=True, max_length=50, help_text='')
    user = db.ReferenceField(User, required=True, help_text='')
    item_summary = db.StringField(required=True, max_length=120, help_text='')
    price = db.StringField(required=True, max_length=50, help_text='')
    details = db.StringField(required=True, help_text='subject')
    image = db.StringField(required=False, max_length=200,
                           default='static/img/256px-Weiser_State_Forest_Walking_Path.jpg')
    sold = db.BooleanField(required=True, default=False)
    negotiable = db.BooleanField(required=True, default=False)

    meta = {'queryset_class': CustomQuerySet}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo()
        data["user"] = self.user.first_name + ' ' + self.user.last_name
        return json_util.dumps(data, *args, **kwargs)


class Service(db.Document):
    building = db.StringField(required=True, max_length=50, help_text='')
    user = db.ReferenceField(User, required=True, help_text='')
    service_summary = db.StringField(required=True, max_length=120, help_text='')
    details = db.StringField(required=True, help_text='subject')
    image = db.StringField(required=False, max_length=200,
                           default='static/img/256px-Weiser_State_Forest_Walking_Path.jpg')
    discontinue = db.BooleanField(required=True, default=False)
    price = db.StringField(required=True, max_length=50, help_text='')
    negotiable = db.BooleanField(required=True, default=False)

    meta = {'queryset_class': CustomQuerySet}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo()
        data["user"] = self.user.first_name + ' ' + self.user.last_name
        return json_util.dumps(data, *args, **kwargs)
