from bucket.m_connection import s3_connection, s3_put_object
from bucket.m_config import AWS_S3_BUCKET_NAME, AWS_S3_BUCKET_URL
from datetime import datetime
import os

"""
* 파일 업로드
"""
def file_upload(user, collctionName, f):
    try:
        # 1. lcoal에 파일 저장 - 파일 경로 때문에 저장해야함
        f.save(f.filename)
        
        # 2. 파일명 설정
        name, ext = os.path.splitext(f.filename)
        fileTime = datetime.now().strftime('%Y-%m-%d')
        filename = str(user) + "_" + name + "_" + fileTime + ext
        
        # 3. 버킷 연결
        s3 = s3_connection()
        
        # 4. 버킷에 파일 저장
        ret = s3_put_object(s3, AWS_S3_BUCKET_NAME, f.filename, f'{collctionName}/{filename}')
        location = f'{AWS_S3_BUCKET_URL}/{collctionName}/{filename}'

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
            return False, {"error":"Can't saved in s3 bucket"} #false ->400
        
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        return False, {"error" : str(ex)}  #false -> 400
