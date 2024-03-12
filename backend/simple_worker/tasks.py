import time
from celery import Celery
from celery.utils.log import get_task_logger
import requests
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

    target_server_url = ''
    params = {'age' : age, 'gender' : gender, 'voice_url': file_url, 'request_id' : request_id, 'result_id' : result_id}

    try: 
        # condition output 
        result, message = module.fild_module.read_random_condition(age, gender)
        if result:
            condition_image_url = message['image']
            condition_gif_url = message['gif']
            print(condition_image_url, condition_gif_url)
        else:
            condition_image_url = None
            condition_gif_url = None

            # Update status
            status_to_change = 'Failed'
            result, message = module.db_module.update_mz_request_status(request_id, status_to_change)

        voice_image_url = None
        voice_gif_url = None

        # # voice output
        # response = requests.get(target_server_url, params = params)

        # if response.status_code == 200: # 성공 시 
        #     voice_image_url = response.voice_image_url
        #     voice_gif_url = response.voice_gif_url

        #     # Update status
        #     status_to_change = 'Success'
        #     result, message = module.db_module.update_mz_request_status(request_id, status_to_change)
        #     logger.info(message)

        # else: # 실패 시 
        #     voice_image_url = None
        #     voice_gif_url = None

        #     # Update status
        #     status_to_change = 'Failed'
        #     result, message = module.db_module.update_mz_request_status(request_id, status_to_change)

        # Update result 
        result_to_change = {
            'condition_image_url' : condition_image_url,
            'condition_gif_url' : condition_gif_url,
            'voice_image_url' : voice_image_url,
            'voice_gif_url' : response.voice_image_url
        }
        print(result_to_change)
        result, message = module.db_module.update_mz_result_image_gif(request_id, result_to_change)
        logger.info(message)

    except requests.RequestException as e:
        return f'Request failed with exception: {str(e)}'

    logger.info('Work Finished ')
    # return response.status_code
    return 200

# def s3_list_object(s3, bucket, age, gender):
#     try:
#         prefix = "Dataset/test/SF2F/Condition/selected_image/"
#         contents_list = s3.list_objects(bucket, prefix)['Contents']
#         file_list = [content['Key'] for content in contents_list]
#         condition_file_list = []
#         for file in file_list:
#             _, file_name = file.split('-')
#             idx = file_name.rindex('.')
#             if file_name[idx+1:] == 'jpg' and file_name[:idx] == f'{gender}_{age}':
#                 condition_file_list.append(file)


#     except Exception as e:
#         print(e)
#         return False
#     return True