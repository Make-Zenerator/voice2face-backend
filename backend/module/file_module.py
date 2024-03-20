from bucket.m_connection import minio_connection, minio_put_object
from bucket.m_config import BUCKET_NAME, MINIO_API_HOST
from datetime import datetime
from pytz import timezone
from pydub import AudioSegment
import random 
import os

"""
* 파일 업로드
"""
def file_upload(request_id, result_id, collectionName, f):
    try:
        # 1. 파일 타입 확인
        allowed_formats = ['audio/wav', 'audio/x-wav', 'audio/wave']
        if f.mimetype not in allowed_formats:
            return False, {"error": "Unsupported file format. Only WAV files are allowed."}
        
        # 2. 파일을 WAV 형식으로 변환
        audio = AudioSegment.from_file(f)
        # WAV 형식으로 변환 후 임시 파일로 저장 (원본 파일은 삭제)
        temp_file = f.filename + '.wav'
        audio.export(temp_file, format="wav")
        
        # 3. 파일명 설정
        name, ext = os.path.splitext(temp_file)
        fileTime = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d')
        filename = f"{int(request_id):05}" + "_" + f"{int(result_id):05}" + "_voice_" + fileTime + ext
        
        # 4. 버킷 연결
        storage = minio_connection()
        
        # 5. 버킷에 파일 저장
        ret = minio_put_object(storage, f'{collectionName}/{filename}', temp_file)
        location = f'https://{MINIO_API_HOST}/{BUCKET_NAME}/{collectionName}/{filename}'

        # 6. 임시 파일 삭제
        os.remove(temp_file)
            
        # 7. 버킷에 파일 저장 성공 시
        if ret:
            return 200, location
        else:
            return False, {"error": "Failed to save file in minio bucket."}
        
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        return False, {"error": str(ex)}

# """
# * condition image 및 gif 파일 읽고 랜덤 선정
# """
# def read_random_condition(age, gender):
#     try:
#         # 1. age 반올림
#         age = round(age, -1)
        
#         # 2. 버킷 연결
#         storage = minio_connection()
        
#         # 3. 버킷에서 리스트 가져오기 
#         ret = minio_list_object(storage, age, gender)

#         # 4. 버킷에서 리스트 가져오기 성공 시 랜덤 선정 
#         if ret == False:
#             return False, {"error":"Can't find list"} #false ->400 
#         else:
#             print(ret)
#             choicejpg = random.choice(ret)
#             idx = choicejpg.rindex('.')
#             choicemp4 = choicejpg[:idx] + '.mp4'
#             return True, {"image" : choicejpg, "gif" : choicemp4}
        
#     except Exception as ex:
#         print("******************")
#         print(ex)
#         print("******************")
#         return False, {"error" : str(ex)}  #false -> 400