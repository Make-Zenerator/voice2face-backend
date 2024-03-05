from flask import request 
from db.enum_classes import ScopeClass, StatusClass, FaceTypeClass, SchemaName
import module
from static import status_code
from module import db_module, file_module
from celery import Celery
from db.db_config import USERNAME, PASSWORD, HOST, DATABASE

# Create a Celery instance named 'celery_app'
celery = Celery('tasks', broker='amqp://admin:mypass@rabbit:5672')

# Configure Celery settings
celery.conf.update(
    # Configure the result backend using MySQL
    CELERY_RESULT_BACKEND=f'db+mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}',
    
    # Set the task serializer to JSON
    CELERY_TASK_SERIALIZER='json',
    
    # Do not ignore results (set to False)
    CELERY_IGNORE_RESULT=False,
)

################### MZ REQUEST ###################
"""
* TODO mz request upload
"""
def upload_mz_request():
    try:
        token = request.headers.get('Token')
        user = module.token.get_user(token)
        if user == False:
            return 401, {"error": status_code.token_error}
        
        age = request.form.get('age')
        if age == None or not age.isdigit():
            return 404, {"error": f'{status_code.field_error}age'}
        gender = request.form.get('gender')
        if gender == None or (gender != 'man' and gender != 'woman'):
            return 404, {"error": f'{status_code.field_error}gender'}
        status = request.form.get('status')
        ata = request.form.get('ata')
        
        if 'file' not in request.files:
            return 404, {"error": f'{status_code.field_error}file'} 
        filename = request.files['file'].filename
        if filename == None or filename == '':
            return 404, {"error": f'{status_code.field_error}file'}
        f = request.files['file']
        file_result, location = file_module.file_upload(user, SchemaName.mzRequest.value, f)
        if file_result == False:
            return 400, location
        result, message = module.db_module.create_mz_request(user, age, gender, location, status, ata)

        celery_task_id = celery.send_task('tasks.run_mz', kwargs= 
                    {
                        'request_id' : message['mz_request_id'],
                        'result_id' : message['mz_result_id'],
                        'age' : age,
                        'gender' : gender,
                        'file_url' : location
                    })
        
        print("==========================")
        print(celery_task_id)
        print("==========================")
        message["celery_task_id"] = str(celery_task_id)

        return result, message
    except Exception as ex:
        print(ex)
        return 400, {"error": str(ex)}

"""
* mz request get
"""
def get_mz_request(mz_request_id):
    try:
        token = request.headers.get("Token")
        user_id = module.token.get_user(token)
        if user_id == False:
            return 401, {"error": status_code.token_error}
        result, message = module.db_module.read_mz_request(mz_request_id, user_id)
        return result, message
    except Exception as ex:
        print(ex)
        return 400, {"error": str(ex)}

"""
* mz request list get
"""
def get_mz_request_list():
    try:
        token = request.headers.get("Token")
        user_id = module.token.get_user(token)
        if user_id == False:
            return 401, {"error": status_code.token_error}
        result, message = module.db_module.read_mz_request_list(user_id)
        return result, message
    except Exception as ex:
        print(ex)
        return 400, {"error": str(ex)}

################### MZ RESULT ###################
"""
* TODO mz result regenerate
"""
def regenerate_mz_result(mz_request_id):
    try:
        token = request.headers.get("Token")
        user_id = module.token.get_user(token)
        if user_id == False:
            return 401, {"error": status_code.token_error}
        result, mz_result_id = module.db_module.create_mz_result(mz_request_id)
        return result, {"mz_request_id" : str(mz_request_id), "regenerate_mz_result_id" : str(mz_result_id)}
    except Exception as ex:
        print(ex)
        return 400, {"error": str(ex)}

"""
* mz result get
"""
def get_mz_result(mz_request_id, mz_result_id):
    try:
        token = request.headers.get("Token")
        user_id = module.token.get_user(token)
        if user_id == False:
            return 401, {"error": status_code.token_error}
        result, message = module.db_module.read_mz_result(mz_request_id, mz_result_id)
        return result, message
    except Exception as ex:
        print(ex)
        return 400, {"error": str(ex)}

"""
* mz result rating update
"""
def update_mz_result_rating(mz_request_id, mz_result_id):
    try:
        token = request.headers.get("Token")
        user_id = module.token.get_user(token)
        if user_id == False:
            return 401, {"error": status_code.token_error}
        
        condition_image_rating = request.form.get('condition_image_rating')
        if condition_image_rating == None or not condition_image_rating.isdigit():
            return 404, {"error": f'{status_code.field_error}condition_image_rating'}
        condition_gif_rating = request.form.get('condition_gif_rating')
        if condition_gif_rating == None or not condition_gif_rating.isdigit():
            return 404, {"error": f'{status_code.field_error}condition_gif_rating'}
        voice_image_rating = request.form.get('voice_image_rating')
        if voice_image_rating == None or not voice_image_rating.isdigit():
            return 404, {"error": f'{status_code.field_error}voice_image_rating'}
        voice_gif_rating = request.form.get('voice_gif_rating')
        if voice_gif_rating == None or not voice_gif_rating.isdigit():
            return 404, {"error": f'{status_code.field_error}voice_gif_rating'}

        result, message = module.db_module.update_mz_result_rating(mz_request_id, mz_result_id, condition_image_rating, condition_gif_rating, voice_image_rating, voice_gif_rating)
        return result, message
    except Exception as ex:
        print(ex)
        return 400, {"error": str(ex)}


# 1. 백엔드에 샐러리 ID가 있다면 샐러리 ID와 요청해야하는 request_id를 함께 넘겨주기
# 2. 백엔드에서는 result ID로 조회
#     1) 만약 DB 존재한다면 -> DB에서 찾은 정보 바로 return
#     2) 존재하지 않는다면 -> status 조회 후 SUCCESS가 나오는 경우, result_db에 저장하고 return


# """
# * celery status
# * Define a route for getting the status of a task
# """
# def get_celery_task_status(mz_request_id, task_id):
#     try:
#         token = request.headers.get("Token")
#         user_id = module.token.get_user(token)
#         if user_id == False:
#             return 401, {"error": status_code.token_error}
#         result, message = module.db_module.read_mz_request(mz_request_id, user_id)
#         if result == 200:
#             # Get the status of the task using the task ID
#             task_status = celery.AsyncResult(task_id).status
#             # Update status in DB 
#             try:
#                 result, message = module.db_module.update_mz_request_status(mz_request_id, task_status)
#             except Exception as ex:
#                 print(ex)
#                 return 400, {"error": str(ex)}

#             # Return the task status as a JSON response
#             return 200, {'Task Status': task_status}
#         else:
#             return 400, {'Cannot find mz_request'}
#     except Exception as ex:
#         print(ex)
#         return 400, {"error": str(ex)}

# """
# * celery result
# * Define a route for getting the result of a completed task
# """
# def get_celery_result_done(mz_request_id, task_id):
#     try:
#         token = request.headers.get("Token")
#         user_id = module.token.get_user(token)
#         if user_id == False:
#             return 401, {"error": status_code.token_error}
#         result, message = module.db_module.read_mz_request(mz_request_id, user_id)
#         if result == 200:
#             # Get the result of the task using the task ID
#             task_result = celery.AsyncResult(task_id).result
            
#             # Update image and gif in result record
#             try:
#                 result, message = module.db_module.update_mz_result_image_gif(task_result)
#             except Exception as ex:
#                 print(ex)
#                 return 400, {"error": str(ex)}

#             # Return the task result as a JSON response
#             return 200, {'Task Result': task_result}
#         else:
#             return 400, {'Cannot find mz_request'}
#     except Exception as ex:
#         print(ex)
#         return 400, {"error": str(ex)}

# """
# * Whitelist face image delete
# """
# def delete_whitelist_face_image(whitelistFaceId, _id):
#     try:
#         token = request.headers.get('Token')
#         user = module.token.get_user(token)
#         if user == False:
#             return 401, {"error": status_code.token_error}
#         result, message = module.db_module.delete_whitelist_face_image(whitelistFaceId, _id)
#         return result, message
#     except Exception as ex:
#         print(ex)
#         return 400, {"error": str(ex)}

# ################### VIDEO ###################

# """
# * origin video upload
# """
# def origin_video_upload():
#     try:
#         token = request.headers.get('Token')
#         user = module.token.get_user(token)
#         if user == False:
#             return 401, {"error": status_code.token_error}
#         if 'file' not in request.files:
#             return 404, {"error": f'{status_code.field_error}file'}
#         filename = request.files['file'].filename
#         if filename == None or filename == '':
#             return 404, {"error": f'{status_code.field_error}file'}
#         f = request.files['file']
#         fileResult, location = file_module.file_upload(user, SchemaName.video.value, f)
#         if fileResult == False:
#             return fileResult, location
#         result, message = module.db_module.create_video(user, location)
#         if result == True: ###### result-> result == 200
#             return 200, {"id" : message, "url": location}
#         else:
#             return 400, message
#     except Exception as ex:    
#         print(ex)
#         return 400, {"error": str(ex)}
    
# """
# * video delete
# """
# def delete_video(_id):
#     try:
#         token = request.headers.get('Token')
#         user = module.token.get_user(token)
#         if user == False:
#             return False, {"error": status_code.token_error}
#         result, message = db_module.delete_video(user, _id)
#         return result, message
#     except Exception as ex:    
#         print(ex)
#         return False, {"error": str(ex)}

# """
# * update video before save s3
# """
# def update_video_upload():
#     try:
#         token = request.headers.get('Token')
#         user = module.token.get_user(token)
#         if user == False:
#             return False, {"error": status_code.token_error}
        
#         # video id가져옴
#         videoId = request.form.get('video_id')
#         if videoId == None or videoId == '':
#             return False, {"error": f'{status_code.field_error}video_id'}

#         # video url 찾기
#         result, videoUrl = db_module.read_origin_video(videoId, user)
#         if result == False:
#             return result, videoUrl

#         # faceType 가져옴
#         faceType = request.form.get('face_type')
#         if faceType == None or faceType == '':
#             return False, {"error": f'{status_code.field_error}face_type'}
        
#         if faceType != FaceTypeClass.character.value and faceType != FaceTypeClass.mosaic.value:
#             return False, {"error": f'{status_code.enum_class_error}face_type'}

#         # blockCharacterId 선택적으로 가져옴
#         if faceType == FaceTypeClass.character.value:
#             blockCharacterId = request.form.get('block_character_id')
#             if blockCharacterId == None or blockCharacterId == '':
#                 return False, {"error": f'{status_code.field_error}block_character_id'}
#             result, blockCharacterImg = db_module.read_block_character_url(blockCharacterId)
#             if result == False:
#                 return result, blockCharacterImg
#         else:
#             blockCharacterId = None
#             blockCharacterImg = None
        
#         # TODO - whitelistFaceId 없을 경우에 대한 것 처리하기
#         whitelistFaceId = request.form.getlist("whitelist_face_id")
#         result, whitelistFaceImgList = db_module.read_whitelist_face_url(user, whitelistFaceId)
#         if result == False:
#             return result, whitelistFaceImgList

#         # True or False 리턴
#         result, message = db_module.update_video(videoId, user, faceType, whitelistFaceId, blockCharacterId) # ID를 받아와서 찾은다음에 url

#         if result == True:
#             if faceType == FaceTypeClass.mosaic.value:
#                 task = celery.send_task('tasks.run_mosaic', kwargs= 
#                     {
#                         'whitelistFaceImgList' : whitelistFaceImgList, # url 리스트
#                         'videoUrl' : videoUrl,
#                         "user" : str(user)
#                     })
#                 result2, message = db_module.update_video_celery(videoId, user, task, task.status)

#                 if result2 == True:
#                     return True, {"id" : str(task.id)}
#                 else:
#                     return False, {"error":status_code.update_02_fail}
#             elif faceType == FaceTypeClass.character.value:
#                 task = celery.send_task('tasks.run_character', kwargs=
#                     {
#                         'whitelistFaceImgList' : whitelistFaceImgList, 
#                         'blockCharacterImgUrl' : blockCharacterImg, 
#                         'videoUrl' : videoUrl,
#                         "user" : str(user)
#                     })
#                 result2, message = db_module.update_video_celery(videoId, user, task, task.status)

#                 if result2 == True:
#                     return True, {"id" : str(task.id)}
#                 else:
#                     return False, {"error":status_code.update_02_fail}
#         else:
#             return result, message
#     except Exception as ex:
#         print(ex)
#         return False, {"error": str(ex)}

# """
# * 셀러리 id를 통해 상태 체크
# """
# def get_after_video_status(taskId):
#     try:
#         token = request.headers.get("Token")
#         user = module.token.get_user(token)
#         if user == False:
#             return False, {"error": status_code.token_error}
#         result, message = db_module.read_celery_status(user, taskId)
#         if message == StatusClass.failure.value:
#             status = celery.AsyncResult(taskId, app=celery)
#             result2 = db_module.update_video_celery_failure(user, taskId) #video컬렉션의 status를 FAILURE로 업데이트
#             if result2 == True:
#                 return True, {"status" : StatusClass.failure.value} #셀러리의 결과과 failure이고, video 컬렉션의 status 업데이트를 성공한 경우
#             else:
#                 return False, {"error", status_code.update_02_fail} #셀러리의 결과과 failure이고, video 컬렉션의 status 업데이트를 실패한 경우
#         elif result == 0:
#             return True, {"status" : StatusClass.pending.value} #PENDING
#         else:
#             return True, {"status" : message} #SUCCESS
#     except Exception as ex:
#         print(ex)
#         return False, {"error": str(ex)}
    
# """
# * 특정 유저에 대한 비디오 결과 모두 조회하기
# """
# def get_multiple_after_video():
#     try:
#         token = request.headers.get("Token")
#         user = module.token.get_user(token)
#         if user == False:
#             return False, {"error": status_code.token_error}
#         result, message = module.db_module.read_proccessed_video(user)
#         return result, message
#     except Exception as ex:
#         print(ex)
#         return False, {"error": str(ex)}

# """
# * read celery task status
# """
# def read_celery_task_status(taskId):
#     try:
#         status = celery.AsyncResult(taskId, app=celery)
#         if status == StatusClass.success:
#             result = celery.AsyncResult(taskId).result
#             return True, {"status", result}
#         else:
#             return False, {"status", status}
#     except Exception as ex:
#         print(ex)
#         return False, {"error": str(ex)}
