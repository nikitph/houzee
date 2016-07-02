from flask import render_template, g
from flask.ext.mongoengine.wtf import model_form

__author__ = 'Omkareshwar'


def cruder(req, usr_model_class, template, route_name, display_name, field_args=None, list_args=None,
           key_id='', cache_class=''):
    mode = get_mode(req)
    # 1 = c, 2= r, 3=u, 4=d, 5=l

    if mode == 1:
        print(1)
        usr_obj_form = model_form(usr_model_class, field_args=field_args)
        print(2)
        form = usr_obj_form(req.form)
        print(form)
        return render_template(template, form=form, mode=1, routename=route_name, displayname=display_name,
                               key_id=key_id, cache_class=cache_class)

    elif mode == 2:
        mod_obj = usr_model_class.objects(id=req.args.get('id')).first()
        usr_obj_form = model_form(usr_model_class, field_args=field_args)
        form = usr_obj_form(req.form, mod_obj)
        return render_template(template, form=form, mode=2, routename=route_name, displayname=display_name,
                               key_id=key_id)

    elif mode == 3:
        mod_obj = usr_model_class.objects(id=req.args.get('id')).first()
        usr_obj_form = model_form(usr_model_class, field_args=field_args)
        form = usr_obj_form(req.form, mod_obj)
        return render_template(template, form=form, mode=3, routename=route_name, displayname=display_name,
                               key_id=key_id, cache_class=cache_class)

    elif mode == 4:
        mod_obj = usr_model_class.objects(id=req.args.get('id')).first()
        mod_obj.delete()
        return render_template(template, mode=4, routename=route_name, displayname=display_name, key_id=key_id)

    elif mode == 5:
        mod_obj = model_form(usr_model_class, field_args=list_args)
        form = mod_obj(req.form)
        return render_template(route_name + 'list.html',
                               msg=usr_model_class.objects(building=str(g.user.buildingid)).to_json(), form=form,
                               routename=route_name, displayname=display_name, key_id=key_id)

    else:
        usr_obj_form = model_form(usr_model_class, field_args=field_args)
        form = usr_obj_form(req.form)
        return render_template(template, form=form, mode=1, routename=route_name, displayname=display_name)


def get_mode(req):
    mode = req.args.get('m')
    if mode == 'c':
        return 1
    elif mode == 'r':
        return 2
    elif mode == 'u':
        return 3
    elif mode == 'd':
        return 4
    elif mode == 'l':
        return 5


def poster(request, usr_model_class):
    if request.args.get('id') is None:
        obj_form = model_form(usr_model_class)
        form = obj_form(request.form)
    else:
        mod_obj = usr_model_class.objects(id=str(request.args.get('id'))).first()
        usr_obj_form = model_form(usr_model_class)
        form = usr_obj_form(request.form, mod_obj)

    return str(form.save().id)
