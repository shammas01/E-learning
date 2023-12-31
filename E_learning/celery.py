import os
from celery.schedules import crontab
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'E_learning.settings')

app = Celery('E_learning')

#we are using asia/kolkata time so we are making it False
app.conf.enable_utc=False
app.conf.update(timezone='Asia/Kolkata')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.

app.autodiscover_tasks() #(lambda: settings.INSTALLED_APPS) <> add this into your autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


#celery beat settings
app.conf.beat_schedule = {
    'send-mail-everyday-at-7': {
        'task': 'live.tasks.send_mail_func',
        'schedule': crontab(hour=7, minute=0),
        
    },
    'send-reminder-everyday-at-7': {
        'task': 'userdashboad.tasks.send_email_reminder',
        'schedule': crontab(hour=17, minute=0), 
        
    }
}