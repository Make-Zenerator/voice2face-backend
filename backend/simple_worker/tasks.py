import time
from celery import Celery
from celery.utils.log import get_task_logger
# import requests
from db_config import USERNAME, PASSWORD, HOST, DATABASE

logger = get_task_logger(__name__)

# Create a Celery instance named 'celery_app'
# celery = Celery('tasks',backend='db+mysql+pymysql://root:rootpwd@mysql-db:3306/MZ', broker='amqp://admin:mypass@rabbit:5672')
celery = Celery('tasks',backend=f'db+mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}', broker='amqp://admin:mypass@rabbit:5672')

@celery.task()
def run_mz(age, gender, file_url):
    logger.info('Got Request - Starting work ')
    time.sleep(4)
    logger.info(age, gender, file_url)
    logger.info('Work Finished ')
    return 200, "SUCCESS", "PERFECT"
