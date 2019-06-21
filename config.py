# config.py
import os


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = os.environ["0SmGhlE2E7cKxztXCR3u7w"]
    CELERY_RESULT_BACKEND = os.environ['REDIS_URL']
    CELERY_BROKER_URL = os.environ['REDIS_URL']
