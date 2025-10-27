from celery import Celery
from celery.schedules import crontab

celery = Celery(__name__,broker='redis://localhost:6379/0', backend = 'redis://localhost:6379/0')

CELERY_BEAT_SCHEDULE = {
    'generate_monthly_reports':{
        'task': 'tasks.generate_monthly_reports',
        #'schedule': crontab(day_of_month='1')
        'schedule': 10.0
    },
    'daily-reminders':{
        'task': 'tasks.send_daily_reminders',
        'schedule':crontab(hour= 18)

    }
}


celery.conf.beat_schedule = CELERY_BEAT_SCHEDULE