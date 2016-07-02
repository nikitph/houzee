from bson import json_util
from mongoengine import EmbeddedDocumentField, ListField, Document, DynamicDocument, ReferenceField, QuerySet
from wtforms import FieldList, StringField
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


class Resident(db.Document):
    building = db.StringField(required=True, max_length=100, help_text='')
    resident_name = db.StringField(required=True, max_length=20, help_text='perm_identity')
    apartment = db.ReferenceField(Apartment, required=True, help_text='activateSlave(this);')
    phone = db.StringField(required=True, max_length=20, help_text='phone')
    email = db.StringField(required=True, max_length=20, help_text='email')
    date_of_birth = db.StringField(required=True, max_length=20, help_text='cake')
    related = db.DictField(required=False)
    image = db.StringField(required=False, max_length=200,
                           default='static/img/256px-Weiser_State_Forest_Walking_Path.jpg')

    def __str__(self):
        return self.resident_name

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
    # description = db.StringField(required=True, help_text='description')

    def __str__(self):
        return self.event_name

    __rpr__ = __str__


class BulkNotification(db.Document):
    building = db.StringField(required=True, max_length=50, help_text='')
    subject = db.StringField(required=True, max_length=200, help_text='mail_outline')
    body = db.StringField(required=True, verbose_name='Notification Message', help_text='subject')


# class Conveyance(db.Document):
#     school = db.StringField(required=True, max_length=50)
#     registration_number = db.StringField(required=True, max_length=50, help_text='confirmation_number')
#     total_seats = db.StringField(required=True, max_length=5, help_text='event_seat')
#     maximum_capacity = db.StringField(required=True, max_length=50, help_text='arrow_upward')
#     person_for_contact = db.StringField(required=True, max_length=50, help_text='perm_identity')
#     contact_phone = db.StringField(required=True, max_length=50, help_text='phone')
#     other_details = db.StringField(required=True, help_text='description')
#
#     def __str__(self):
#         return self.registration_number
#
#     __rpr__ = __str__
#
#
# class Driver(db.Document):
#     school = db.StringField(required=True, max_length=50)
#     driver_name = db.StringField(required=True, max_length=50, help_text='perm_identity')
#     street_address = db.StringField(required=True, help_text='location_on')
#     city = db.StringField(required=True, max_length=20, help_text='location_city')
#     state = db.StringField(required=True, max_length=20, help_text='navigation')
#     pincode = db.StringField(required=True, max_length=20, help_text='local_parking')
#     date_of_birth = db.StringField(required=True, max_length=20, help_text='cake')
#     contact_phone = db.StringField(required=True, max_length=50, help_text='phone')
#     license_number = db.StringField(required=True, max_length=50, help_text='vpn_key')
#     other_details = db.StringField(required=True, help_text='description')
#     image = db.StringField(required=False, max_length=200,
#                            default='static/img/256px-Weiser_State_Forest_Walking_Path.jpg')
#
#     def __str__(self):
#         return self.driver_name
#
#     __rpr__ = __str__
#
#
# class BusStop(db.Document):
#     school = db.StringField(required=True, max_length=50)
#     stop_name = db.StringField(required=True, max_length=50, help_text='perm_identity')
#     stop_address = db.StringField(required=True, help_text='location_on')
#     landmark = db.StringField(required=True, max_length=150, help_text='navigation')
#     pick_up_time = db.StringField(required=True, max_length=50, help_text='hourglass_full')
#
#     def __str__(self):
#         return self.stop_name
#
#     __rpr__ = __str__
#
#
# class BusRoute(db.Document):
#     school = db.StringField(required=True, max_length=50)
#     route_name = db.StringField(required=True, max_length=50, help_text='perm_identity')
#     driver = db.ReferenceField(Driver, required=True)
#     vehicle = db.ReferenceField(Conveyance, required=True)
#     stops = db.ListField(ReferenceField(BusStop, required=True))
#
#     def __str__(self):
#         return self.route_name
#
#     __rpr__ = __str__
#
#
# class Transportation(db.Document):
#     route = db.ReferenceField(BusRoute, required=True, help_text='activateSlave(this);')
#     stop = db.ReferenceField(BusStop, required=True)
#     student_id = db.StringField(required=True, max_length=50, help_text='')
#
#     def save(self, *args, **kwargs):
#         super(Transportation, self).save(*args, **kwargs)
#         stu = Student.objects(id=self.student_id).first()
#         keys = {str(self.id): 'transportation'}
#         set_new = dict((("set__related__%s" % k, v) for k, v in keys.iteritems()))
#         stu.update(**set_new)
#
#
# class Hostel(db.Document):
#     school = db.StringField(required=True, max_length=50)
#     hostel_name = db.StringField(required=True, max_length=50, help_text='hotel')
#     street_address = db.StringField(required=True, help_text='location_on')
#     city = db.StringField(required=True, max_length=20, help_text='location_city')
#     state = db.StringField(required=True, max_length=20, help_text='navigation')
#     pincode = db.StringField(required=True, max_length=20, help_text='local_parking')
#     phone = db.StringField(required=True, max_length=50, help_text='phone', verbose_name='Hostel Phone')
#     warden_name = db.StringField(required=True, max_length=50, help_text='perm_identity')
#     warden_phone = db.StringField(required=True, max_length=50, help_text='phone', verbose_name='Warden Phone')
#
#     def __str__(self):
#         return self.hostel_name
#
#     __rpr__ = __str__
#
#
# class HostelRoom(db.Document):
#     school = db.StringField(required=True, max_length=50)
#     hostel = db.ReferenceField(Hostel, required=True)
#     room_id = db.StringField(required=True, max_length=50, help_text='perm_identity')
#     floor = db.StringField(required=True, max_length=50, help_text='view_agenda')
#     total_beds = db.StringField(required=True, max_length=50, help_text='hotel')
#
#     def __str__(self):
#         return self.room_id
#
#     __rpr__ = __str__
#
#     meta = {'queryset_class': CustomQuerySet}
#
#     def to_json(self, *args, **kwargs):
#         data = self.to_mongo()
#         data["hostel"] = self.hostel.hostel_name
#         return json_util.dumps(data, *args, **kwargs)
#
#
# class HostelAssignment(db.Document):
#     hostel = db.ReferenceField(Hostel, required=True, help_text='activateSlave(this);')
#     room = db.ReferenceField(HostelRoom, required=True)
#     student_id = db.StringField(required=True, max_length=50, help_text='')
#
#     def save(self, *args, **kwargs):
#         super(HostelAssignment, self).save(*args, **kwargs)
#         stu = Student.objects(id=self.student_id).first()
#         keys = {str(self.id): 'hostel'}
#         set_new = dict((("set__related__%s" % k, v) for k, v in keys.iteritems()))
#         stu.update(**set_new)



