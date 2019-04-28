cd /D D:\PycharmProjects\RGSManager

celery -A celery_app worker -l info
celery -A celery_app beat -l info