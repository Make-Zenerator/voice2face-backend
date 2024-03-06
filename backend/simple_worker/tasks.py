import time
from celery import Celery
from celery.utils.log import get_task_logger
# import requests
from db_config import USERNAME, PASSWORD, HOST, DATABASE
import requests
import module

logger = get_task_logger(__name__)

# Create a Celery instance named 'celery_app'
# celery = Celery('tasks',backend='db+mysql+pymysql://root:rootpwd@mysql-db:3306/MZ', broker='amqp://admin:mypass@rabbit:5672')
celery = Celery('tasks',backend=f'db+mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}', broker='amqp://admin:mypass@rabbit:5672')

@celery.task()
def run_mz(request_id, result_id, age, gender, file_url):
    logger.info('Got Request - Starting work')
    time.sleep(4)
    logger.info(age, gender, file_url)
    # target_server_url = ''
    # params = {'age' : age, 'gender' : gender, 'voice_url': file_url}
    # try: # ML server로 요청 보내기 
    #     response = requests.get(target_server_url, params = params)
    #     # response은 condition_image_url, condition_gif_url, voice_image_url, voice_gif_url로 구성 
    #     if response.status_code == 200: # 성공 시 
    #         response.request_id = request_id
    #         response.result_id = result_id

    #         # Update status
    #         status_to_change = 'SUCCESS'
    #         result, message = module.db_module.update_mz_request_status(request_id, status_to_change)
    #         logger.info(message)

    #         # Update result 
    #         result_to_change = {
    #             'condition_image_url' : response.condition_image_url,
    #             'condition_gif_url' : response.condition_gif_url,
    #             'voice_image_url' : response.voice_image_url,
    #             'voice_gif_url' : response.voice_image_url
    #         }
    #         result, message = module.db_module.update_mz_result_image_gif(request_id, result_to_change)
    #         logger.info(message)

    #     else: # 실패 시 
    #         # Update status
    #         status_to_change = 'FAILED'
    #         result, message = module.db_module.update_mz_request_status(request_id, status_to_change)

    # except requests.RequestException as e:
    #     return f'Request failed with exception: {str(e)}'

    logger.info('Work Finished ')
    # return response.status_code
    return 200
