import datetime

from flask import Blueprint, request, redirect, url_for, g, jsonify

from flask.ext.security import login_required, current_user, roles_required, user_registered
from flask.ext.security.script import CreateUserCommand, AddRoleCommand
from flask.ext.sse import sse
from flask.templating import render_template
from werkzeug.utils import secure_filename
import wtforms
from flask.ext.mongoengine.wtf import model_form
from tasks import email

from public.models import *
from user.models import User, Role, Notification
from user.utility import cruder, poster

bp_user = Blueprint('users', __name__, static_folder='../static')


@bp_user.before_request
def before_request():
    g.user = current_user


@user_registered.connect
def on_user_registration(sender, user, **extra):
    AddRoleCommand().run(user_identifier=str(user.email), role_name='resident')


@bp_user.route('/')
def index():
    return render_template('index.html')


@bp_user.route('/send')
def send_message():
    sse.publish({"subject": '1', "id": '2'}, type='greeting')
    return "Message sent!"


@login_required
@bp_user.route('/setupd', methods=['GET'])
def setupd():
    bid = Building.objects(id=g.user.buildingid).only('township').first()
    return render_template('setupd.html', bid=str(bid.township))


@login_required
@bp_user.route('/township', methods=['GET', 'POST'])
def township():
    if request.method == 'GET':
        return cruder(request, Township, 'township.html', 'township', 'Township')

    else:
        obj_form = model_form(Township)
        form = obj_form(request.form)
        if request.args['s'] == 't':
            AddRoleCommand().run(user_identifier=str(g.user.email), role_name='manager')
            return redirect(url_for('.building', m='c', s='t', iid=str(form.save().id)))
        return redirect(url_for('.township', m='r', id=str(form.save().id)))


@bp_user.route('/building', methods=['GET', 'POST'])
@roles_required('manager')
def building():
    if request.method == 'GET':
        # fields to be hidden come here
        field_args = {'user': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, Building, 'building.html', 'building', 'Building', field_args)

    else:
        obj_form = model_form(Building)
        form = obj_form(request.form)
        sid = form.save().id
        User.objects(id=g.user.get_id()).update_one(set__building=request.form['building_name'])
        User.objects(id=g.user.get_id()).update_one(set__buildingid=str(sid))
        g.user.reload()
        if request.args['s'] == 't':
            return render_template('complete.html')
        return redirect(url_for('.building', m='r', id=str(sid)))


@login_required
@bp_user.route('/apartment', methods=['GET', 'POST'])
@roles_required('manager')
def apartment():
    if request.method == 'GET':
        field_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, Apartment, 'apartment.html', 'apartment', 'Apartment', field_args, list_args,
                      g.user.buildingid)

    else:
        return redirect(url_for('.apartment', m='r', id=poster(request, Apartment)))


@login_required
@bp_user.route('/resident', methods=['GET', 'POST'])
def resident():
    if request.method == 'GET':
        field_args = {'related': {'widget': wtforms.widgets.HiddenInput()},
                      'image': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'street_address': {'widget': wtforms.widgets.HiddenInput()},
                     'image': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, Resident, 'resident.html', 'resident', 'Resident', field_args, list_args
                      )

    else:
        rid = poster(request, Resident)
        CreateUserCommand().run(email=str(request.form['email']), password=str(request.form['phone']), active=1)
        AddRoleCommand().run(user_identifier=str(request.form['email']), role_name='resident')
        return redirect(url_for('.resident', m='r', id=rid))


# @login_required
# @bp_user.route('/parent', methods=['GET', 'POST'])
# def parent():
#     if request.method == 'GET':
#         field_args = {'resident_id': {'widget': wtforms.widgets.HiddenInput()}}
#         return cruder(request, Parent, 'parent.html', 'parent', 'Parent', field_args)
#
#     else:
#         return redirect(url_for('.parent', m='r', id=poster(request, Parent)))
#
#
# @login_required
# @bp_user.route('/scholarship', methods=['GET', 'POST'])
# def scholarship():
#     if request.method == 'GET':
#         field_args = {'resident_id': {'widget': wtforms.widgets.HiddenInput()}}
#         return cruder(request, Scholarship, 'scholarship.html', 'scholarship', 'Scholarship', field_args)
#
#     else:
#         return redirect(url_for('.scholarship', m='r', id=poster(request, Scholarship)))
#
#
# @login_required
# @bp_user.route('/award', methods=['GET', 'POST'])
# def award():
#     if request.method == 'GET':
#         field_args = {'resident_id': {'widget': wtforms.widgets.HiddenInput()}}
#         return cruder(request, Award, 'award.html', 'award', 'Award', field_args)
#
#     else:
#         return redirect(url_for('.award', m='r', id=poster(request, Award)))
#
#
# @login_required
# @bp_user.route('/transportation', methods=['GET', 'POST'])
# def transportation():
#     if request.method == 'GET':
#         field_args = {'resident_id': {'widget': wtforms.widgets.HiddenInput()}}
#         list_args = {'resident_id': {'widget': wtforms.widgets.HiddenInput()}}
#         return cruder(request, Transportation, 'transportation.html', 'transportation',
#                       'Transportation', field_args,
#                       list_args, request.args['sid'])
#
#     else:
#         return redirect(url_for('.transportation', m='r', id=poster(request, Transportation), sid=request.args['sid']))
#
#
# @login_required
# @bp_user.route('/hostelassignment', methods=['GET', 'POST'])
# def hostelassignment():
#     if request.method == 'GET':
#         field_args = {'resident_id': {'widget': wtforms.widgets.HiddenInput()}}
#         list_args = {'resident_id': {'widget': wtforms.widgets.HiddenInput()}}
#         return cruder(request, HostelAssignment, 'hostelassignment.html', 'hostelassignment',
#                       'Hostel Assignment', field_args,
#                       list_args, request.args['sid'])
#
#     else:
#         return redirect(url_for('.hostelassignment', m='r', id=poster(request, HostelAssignment), sid=request.args['sid']))
#
#
# @login_required
# @bp_user.route('/subject', methods=['GET', 'POST'])
# def subject():
#     if request.method == 'GET':
#         field_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
#         list_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
#         return cruder(request, Subject, 'subject.html', 'subject', 'Subject', field_args, list_args, g.user.buildingid)
#
#     else:
#         return redirect(url_for('.subject', m='r', id=poster(request, Subject)))
#
#
# @login_required
# @bp_user.route('/teacher', methods=['GET', 'POST'])
# def teacher():
#     if request.method == 'GET':
#         field_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
#         list_args = {'building': {'widget': wtforms.widgets.HiddenInput()},
#                      'subjects': {'widget': wtforms.widgets.HiddenInput()}}
#         return cruder(request, Teacher, 'teacher.html', 'teacher', 'Teacher', field_args, list_args)
#
#     else:
#         CreateUserCommand().run(email=request.form['email'], password='234765', active=1)
#         AddRoleCommand().run(user_identifier=request.form['email'], role_name='teacher')
#         return redirect(url_for('.teacher', m='r', id=poster(request, Teacher)))


@login_required
@bp_user.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            now = datetime.datetime.now()
            filename = secure_filename(file.filename)
            file.save('static/img/' + filename)
            return jsonify({"filepath": 'static/img/' + filename})


@login_required
@bp_user.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html')

    else:
        User.objects(id=g.user.get_id()).update_one(set__phone=request.form['phone'])
        User.objects(id=g.user.get_id()).update_one(set__address=request.form['address'])
        User.objects(id=g.user.get_id()).update_one(set__image=request.form['image'])
    return redirect(url_for('.resident', m='l'))


# @login_required
# @bp_user.route('/event', methods=['GET', 'POST'])
# def event():
#     if request.method == 'GET':
#         field_args = {'building': {'widget': wtforms.widgets.HiddenInput()}, 'event_for': {'radio': True}}
#         list_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
#         print(g.user.buildingid)
#         return cruder(request, Event, 'event.html', 'event', 'Event', field_args, list_args, g.user.buildingid)
#
#     else:
#         return redirect(url_for('.event', m='r', id=poster(request, Event)))
#
#
# @login_required
# @bp_user.route('/conveyance', methods=['GET', 'POST'])
# def conveyance():
#     if request.method == 'GET':
#         field_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
#         list_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
#         return cruder(request, Conveyance, 'conveyance.html', 'conveyance', 'Conveyance', field_args, list_args,
#                       g.user.buildingid)
#
#     else:
#         return redirect(url_for('.conveyance', m='r', id=poster(request, Conveyance)))
#
#
# @login_required
# @bp_user.route('/driver', methods=['GET', 'POST'])
# def driver():
#     if request.method == 'GET':
#         field_args = {'building': {'widget': wtforms.widgets.HiddenInput()},
#                       'image': {'widget': wtforms.widgets.HiddenInput()}}
#         list_args = {'building': {'widget': wtforms.widgets.HiddenInput()},
#                      'image': {'widget': wtforms.widgets.HiddenInput()}}
#         return cruder(request, Driver, 'driver.html', 'driver', 'Driver', field_args, list_args, g.user.buildingid)
#
#     else:
#         return redirect(url_for('.driver', m='r', id=poster(request, Driver)))
#
#
# @login_required
# @bp_user.route('/busstop', methods=['GET', 'POST'])
# def busstop():
#     if request.method == 'GET':
#         field_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
#         list_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
#         return cruder(request, BusStop, 'busstop.html', 'busstop', 'Bus Stop', field_args, list_args,
#                       g.user.buildingid)
#
#     else:
#         return redirect(url_for('.busstop', m='r', id=poster(request, BusStop)))
#
#
# @login_required
# @bp_user.route('/busroute', methods=['GET', 'POST'])
# def busroute():
#     if request.method == 'GET':
#         field_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
#         list_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
#         return cruder(request, BusRoute, 'busroute.html', 'busroute', 'Bus Route', field_args, list_args,
#                       g.user.buildingid)
#
#     else:
#         return redirect(url_for('.busroute', m='r', id=poster(request, BusRoute)))
#
#
# @login_required
# @bp_user.route('/transportd', methods=['GET'])
# def transportd():
#     vehicle = Conveyance.objects(building=str(g.user.buildingid)).to_json()
#     driver = Driver.objects(building=str(g.user.buildingid)).to_json()
#     stop = BusStop.objects(building=str(g.user.buildingid)).to_json()
#     route = BusRoute.objects(building=str(g.user.buildingid)).to_json()
#     return render_template('transportd.html', vehicle=vehicle, driver=driver, stop=stop, route=route)


@login_required
@bp_user.route('/bulknotify', methods=['GET', 'POST'])
def bulknotify():
    if request.method == 'GET':
        field_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, BulkNotification, 'bulknotify.html', 'bulknotify', 'Bulk Notification', field_args,
                      list_args, g.user.buildingid)

    else:
        obj_form = model_form(BulkNotification)
        form = obj_form(request.form)
        id = str(form.save().id)
        x = Resident.objects.only('email')
        rcp = []
        response = {"subject": form['subject'].data, "id": id}
        notif = Notification(subject=form['subject'].data, url=id, read=False)
        User.objects(id=g.user.get_id()).update_one(add_to_set__notif=notif)
        g.user.reload()

        for s in x:
            rcp.append(str(s.email))

        task = email.apply_async(args=[form['subject'].data, form['body'].data, rcp])
        return redirect(url_for('.bulknotify', m='r', id=id))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ['jpg', 'jpeg']


# @login_required
# @bp_user.route('/hosteld', methods=['GET'])
# def hosteld():
#     hostels = Hostel.objects(building=str(g.user.buildingid)).to_json()
#     room = HostelRoom.objects(building=str(g.user.buildingid)).to_json()
#     return render_template('hosteld.html', hostel=hostels, room=room)
#
#
# @login_required
# @bp_user.route('/hostel', methods=['GET', 'POST'])
# def hostel():
#     if request.method == 'GET':
#         field_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
#         list_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
#         return cruder(request, Hostel, 'hostel.html', 'hostel', 'Hostel', field_args, list_args,
#                       g.user.buildingid)
#
#     else:
#         return redirect(url_for('.hostel', m='r', id=poster(request, Hostel)))
#
#
# @login_required
# @bp_user.route('/hostelroom', methods=['GET', 'POST'])
# def hostelroom():
#     if request.method == 'GET':
#         field_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
#         list_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
#         return cruder(request, HostelRoom, 'hostelroom.html', 'hostelroom', 'Hostel Room', field_args, list_args,
#                       g.user.buildingid)
#
#     else:
#         return redirect(url_for('.hostelroom', m='r', id=poster(request, HostelRoom)))
#
#
# @login_required
# @bp_user.route('/classroom', methods=['GET', 'POST'])
# def classroom():
#     if request.method == 'GET':
#         field_args = {'building': {'widget': wtforms.widgets.HiddenInput()}}
#         list_args = {'building': {'widget': wtforms.widgets.HiddenInput()},
#                      'subjects': {'widget': wtforms.widgets.HiddenInput()}}
#         return cruder(request, ClassRoom, 'classroom.html', 'classroom', 'Class Room', field_args, list_args,
#                       g.user.buildingid)
#
#     else:
#         return redirect(url_for('.classroom', m='r', id=poster(request, ClassRoom)))
#

@bp_user.route('/status/<task_id>')
def taskstatus(task_id):
    task = email.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)
