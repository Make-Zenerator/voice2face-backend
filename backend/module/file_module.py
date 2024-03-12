from bucket.m_connection import minio_connection, minio_put_object
from bucket.m_config import BUCKET_NAME, MINIO_API_HOST
from datetime import datetime
from pytz import timezone
import os

"""
* 파일 업로드
"""
def file_upload(request_id, result_id, collctionName, f):
    try:
        # 1. local에 파일 저장 - 파일 경로 때문에 저장해야함
        f.save(f.filename)
        
        # 2. 파일명 설정
        name, ext = os.path.splitext(f.filename)
        fileTime = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d')
        filename = f"{int(request_id):05}" + "_" + f"{int(result_id):05}" + "_voice_" + fileTime + ext
        
        # 3. 버킷 연결
        storage = minio_connection()
        
        # 4. 버킷에 파일 저장
        ret = minio_put_object(storage, f'{collctionName}/{filename}', f.filename)
        location = f'http://{MINIO_API_HOST}/{BUCKET_NAME}/{collctionName}/{filename}'

        # 5. local에 저장된 파일 삭제
        os.remove(f.filename)
            
        # 6. 버킷에 파일 저장 성공 시 진행
        if ret :
            # 6-3. 성공 message return
            if location != None:
                return 200, location #true->200
            else:
                print("Can't find location")
                return False, {"error":"Can't find location"} #false ->400 
        
        # 6. 버킷에 파일 저장 실패 시 진행 (ret == False 일 경우)
        else:
            return False, {"error":"Can't saved in minio bucket"} #false ->400
        
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        return False, {"error" : str(ex)}  #false -> 400