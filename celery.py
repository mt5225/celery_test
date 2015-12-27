from __future__ import absolute_import

from celery import Celery

app = Celery('celery_test',
             broker='amqp://',
             backend='amqp://',
             include=['celery_test.tasks'])

#set task reslut length
app.Task.resultrepr_maxsize = 2000

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERYD_CONCURRENCY=10,
    CELERY_RESULT_BACKEND='celery_test.backends:CustomMongoBackend',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_MONGODB_BACKEND_SETTINGS={
      'database': 'celery',
      'taskmeta_collection': 'taskmeta_collection'
    }
)

if __name__ == '__main__':
    app.start()
