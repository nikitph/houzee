# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_sse import sse
from jinja2 import is_undefined
from settings import ProdConfig
from flask.ext.security import Security, MongoEngineUserDatastore
from user.models import User, Role
from admin.views import UserView, RoleView
from user.forms import ExtendedRegisterForm
from extensions import (
    cache,
    admin,
    db,
    mail,
    debug_toolbar
)
from public.views import bp_public
from user.views import bp_user


def create_app(config_object=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    @app.template_filter('vue')
    def vue(value):
        """
        A filter to tell Jinja2 that a variable is for the AngularJS template
        engine.
        If the variable is undefined, its name will be used in the AngularJS
        template, otherwise, its content will be used.
        """

        if is_undefined(value):
            return '{{ ' + value._undefined_name + ' }}'
        if type(value) is bool:
            value = repr(value).lower()
        return '{{{{{}}}}}'.format(value)

    return app


def register_extensions(app):
    cache.init_app(app)
    db.init_app(app)
    admin.init_app(app)
    register_admin_views(admin)
    user_datastore = MongoEngineUserDatastore(db, User, Role)
    security = Security(app, user_datastore, register_form=ExtendedRegisterForm)
    mail.init_app(app)
    # socketio.init_app(app)
    app.config['DEBUG_TB_PANELS'] = ['flask.ext.mongoengine.panels.MongoDebugPanel',
                                     'flask_debugtoolbar.panels.versions.VersionDebugPanel',
                                     'flask_debugtoolbar.panels.timer.TimerDebugPanel',
                                     'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
                                     'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
                                     'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
                                     'flask_debugtoolbar.panels.template.TemplateDebugPanel',
                                     'flask_debugtoolbar.panels.logger.LoggingPanel',
                                     'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel']
    debug_toolbar.init_app(app)

    return None


def register_blueprints(app):
    app.register_blueprint(bp_public)
    app.register_blueprint(bp_user)
    app.register_blueprint(sse, url_prefix='/stream')
    print(app.url_map)
    return None


def register_admin_views(admin):
    admin.add_view(UserView(User))
    admin.add_view(RoleView(Role))
    return None


def register_errorhandlers(app):
    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None