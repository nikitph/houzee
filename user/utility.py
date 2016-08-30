import wtforms
from flask import render_template, g
from flask.ext.mongoengine.wtf import model_form

__author__ = 'Omkareshwar'


class CrudParams:
    field_args = None
    list_args = None
    key_id = ''
    cache_class = ''
    remove_list = None

    # def __init__(self, *params, **kwargs):
    #     for dictionary in params:
    #         for key in dictionary:
    #             setattr(self, key, dictionary[key])
    #     for key in kwargs:
    #         setattr(self, key, kwargs[key])

    def __init__(self, req, usr_model_class, template, route_name, display_name, field_args=None, list_args=None,
           key_id='', cache_class='', remove_list=None):
        self.req = req
        self.usr_model_class = usr_model_class
        self.template = template
        self.route_name = route_name
        self.display_name = display_name
        self.field_args = field_args
        self.list_args = list_args
        self.key_id = key_id
        self.cache_class = cache_class
        self.remove_list = remove_list


def cruder(crudParamObj):
    mode = get_mode(crudParamObj.req)
    # 1 = c, 2= r, 3=u, 4=d, 5=l

    if mode == 1:
        usr_obj_form = model_form(crudParamObj.usr_model_class, field_args=crudParamObj.field_args)
        form = usr_obj_form(crudParamObj.req.form)
        if crudParamObj.remove_list is not None:
            for f in form:
                if f.name in crudParamObj.remove_list:
                    form._fields.pop(f.name)
        return render_template(crudParamObj.template, form=form, mode=1, routename=crudParamObj.route_name,
                               displayname=crudParamObj.display_name,
                               key_id=crudParamObj.key_id, cache_class=crudParamObj.cache_class)

    elif mode == 2:
        mod_obj = crudParamObj.usr_model_class.objects(id=crudParamObj.req.args.get('id')).first()
        usr_obj_form = model_form(crudParamObj.usr_model_class, field_args=crudParamObj.field_args)
        form = usr_obj_form(crudParamObj.req.form, mod_obj)
        if crudParamObj.remove_list is not None:
            for f in form:
                if f.name in crudParamObj.remove_list:
                    form._fields.pop(f.name)
        return render_template(crudParamObj.template, form=form, mode=2, routename=crudParamObj.route_name,
                               displayname=crudParamObj.display_name,
                               key_id=crudParamObj.key_id)

    elif mode == 3:
        mod_obj = crudParamObj.usr_model_class.objects(id=crudParamObj.req.args.get('id')).first()
        usr_obj_form = model_form(crudParamObj.usr_model_class, field_args=crudParamObj.field_args)
        form = usr_obj_form(crudParamObj.req.form, mod_obj)
        if crudParamObj.remove_list is not None:
            for f in form:
                if f.name in crudParamObj.remove_list:
                    form._fields.pop(f.name)
        return render_template(crudParamObj.template, form=form, mode=3, routename=crudParamObj.route_name,
                               displayname=crudParamObj.display_name,
                               key_id=crudParamObj.key_id, cache_class=crudParamObj.cache_class)

    elif mode == 4:
        mod_obj = crudParamObj.usr_model_class.objects(id=crudParamObj.req.args.get('id')).first()
        mod_obj.delete()
        return render_template(crudParamObj.template, mode=4, routename=crudParamObj.route_name,
                               displayname=crudParamObj.display_name, key_id=crudParamObj.key_id)

    elif mode == 5:
        mod_obj = model_form(crudParamObj.usr_model_class, field_args=crudParamObj.list_args)
        form = mod_obj(crudParamObj.req.form)
        if crudParamObj.remove_list is not None:
            for f in form:
                if f.name in crudParamObj.remove_list:
                    form._fields.pop(f.name)
        return render_template(crudParamObj.route_name + 'list.html',
                               msg=crudParamObj.usr_model_class.objects(building=str(g.user.buildingid)).to_json(),
                               form=form,
                               routename=crudParamObj.route_name, displayname=crudParamObj.display_name,
                               key_id=crudParamObj.key_id)

    else:
        usr_obj_form = model_form(crudParamObj.usr_model_class, field_args=crudParamObj.field_args)
        form = usr_obj_form(crudParamObj.req.form)
        return render_template(crudParamObj.template, form=form, mode=1, routename=crudParamObj.route_name,
                               displayname=crudParamObj.display_name)


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


def arg_builder(field_list):
    farg = {}
    for f in field_list:
        farg[f] = {'widget': wtforms.widgets.HiddenInput()}
    return farg
