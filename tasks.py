from celery import Celery
from celery.task import task, periodic_task
from flask import Flask
from flask.ext.mail import Message
from extensions import mail
from settings import Config, ProdConfig


def make_celery(app):
    celery = Celery(app.import_name, broker=Config.BROKER_URL)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app2(config_object=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    # register_blueprints(app) !imp == otherwise tasks cant be imported in blueprint

    return app


def register_extensions(app):
    mail.init_app(app)


app = create_app2(Config())
celery = make_celery(app)


@task(bind=True)
def email(self, subj, body, rlist):
    with app.app_context():
        print(rlist)
        total = len(rlist)
        for i, s in enumerate(rlist):
            print(s)
            msg = Message(str(subj), recipients=[s])
            msg.body = str(body)
            mail.send(msg)
            self.update_state(state='PROGRESS',
                              meta={'current': i, 'total': total,
                                    'status': 'Email sent to ' + s})
        return {'current': 100, 'total': 100, 'status': 'Task completed!',
                'result': 42}
