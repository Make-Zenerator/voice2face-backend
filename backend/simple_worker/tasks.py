import time
from celery import Celery
from celery.utils.log import get_task_logger
import requests
from db_config import USERNAME, PASSWORD, HOST, DATABASE
import requests
from minio_connection import read_random_condition
from db_connection import Database

logger = get_task_logger(__name__)

# Create a Celery instance named 'celery_app'
# celery = Celery('tasks',backend='db+mysql+pymysql://root:rootpwd@mysql-db:3306/MZ', broker='amqp://admin:mypass@rabbit:5672')
celery = Celery('tasks',backend=f'db+mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}', broker='amqp://admin:mypass@rabbit:5672')
db = Database()

@celery.task()
def run_mz(request_id, result_id, age, gender, file_url):
    logger.info('Got Request - Starting work')
    time.sleep(4)

    target_server_url = 'https://175.106.97.56:3002/makevideo'
    params = {'age' : age, 'gender' : gender, 'voice_url': file_url, 'request_id' : request_id, 'result_id' : result_id}
    logger.info(params)

    try: 
        # condition output 
        result, message = read_random_condition(age, gender)
        if result:
            condition_image_url = str(message['image'])
            condition_gif_url = str(message['gif'])
            logger.info(condition_image_url)
            logger.info(condition_gif_url)

        else:
            # Update status
            status_to_change = 'Failed'
            db.update_mz_request_status(request_id, status_to_change)
            return 400

        # voice output
        response = requests.post(target_server_url, params = params)
        logger.info('response : ', response)

        if response.status_code == 200: # 성공 시 
            voice_image_url = str(response.voice_image_url)
            voice_video_url = str(response.voice_video_url)

        else: # 실패 시 
            # Update status
            status_to_change = 'Failed'
            result, message = db.update_mz_request_status(request_id, status_to_change)
            return 400

        # Update status
        status_to_change = 'Success'
        result, message = db.update_mz_request_status(request_id, status_to_change)
        logger.info(message)

        # Update result 
        result_to_change = {
            'condition_image_url' : condition_image_url,
            'condition_gif_url' : condition_gif_url,
            'voice_image_url' : voice_image_url,
            'voice_gif_url' : voice_video_url
        }
        print(result_to_change)
        db.update_mz_result_image_gif(request_id, result_to_change)

    except requests.RequestException as e:
        return f'Request failed with exception: {str(e)}'

    logger.info('Work Finished ')
    # return response.status_code
    return 200

