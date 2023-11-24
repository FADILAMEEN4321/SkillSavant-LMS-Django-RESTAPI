from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab



# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_lms.settings')

# create a Celery instance and configure it.
app = Celery('backend_lms')

#Disabling default timezone as UTC
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')


# Celery beat settings.
app.conf.beat_schedule = {
    # 'send-email-enrollment':{
    #     'task': 'enrollment.tasks.send_enrollment_emails_tasks',
    #     'schedule': crontab(),
    # }
}


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")