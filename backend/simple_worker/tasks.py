import time
from celery import Celery
from celery.utils.log import get_task_logger
# import requests
from db_config import USERNAME, PASSWORD, HOST, DATABASE
import requests

logger = get_task_logger(__name__)

# Create a Celery instance named 'celery_app'
# celery = Celery('tasks',backend='db+mysql+pymysql://root:rootpwd@mysql-db:3306/MZ', broker='amqp://admin:mypass@rabbit:5672')
celery = Celery('tasks',backend=f'db+mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}', broker='amqp://admin:mypass@rabbit:5672')

@celery.task()
def run_mz(request_id, result_id, age, gender, file_url):
    logger.info('Got Request - Starting work')
    time.sleep(4)
    logger.info(age, gender, file_url)
    target_server_url = ''
    params = {'age' : age, 'gender' : gender, 'voice_url': file_url}
    try: # ML server로 요청 보내기 
        response = requests.get(target_server_url, params = params)
        # response은 condition_image_url, condition_gif_url, voice_image_url, voice_gif_url로 구성 
        if response.status_code == 200: # 성공 시 
            response.request_id = request_id
            response.result_id = result_id
            
            return response
        else: # 실패 시 
            return None
    except requests.RequestException as e:
        return f'Request failed with exception: {str(e)}'


    logger.info('Work Finished ')
    return 200, "SUCCESS", "PERFECT"
