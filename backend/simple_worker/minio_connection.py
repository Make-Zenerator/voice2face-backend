from minio_config import ACCESS_KEY, SECRET_KEY
from minio_config import BUCKET_NAME, MINIO_API_HOST

def minio_connection():
    try:
        storage = Minio(
            MINIO_API_HOST,
            ACCESS_KEY,
            SECRET_KEY,     
            secure=False,
        )
    except Exception as e:
        print(e)
        return False
    else:
        print("storage bucket connected!")
        return storage

def minio_put_object(storage, filename, data):
    '''
    minio bucket에 지정 파일 업로드
    :param minio: 연결된 minio 객체(Minio client)
    :param filename: 파일 위치
    :param data: 데이터
    :return: 성공 시 True, 실패 시 False 반환
    '''
    try:
        storage.fput_object(BUCKET_NAME, filename, data)
        print(f"{filename} is successfully uploaded to bucket {BUCKET_NAME}.")
    except Exception as e:
        print(e)
        return False
    return True

def read_random_condition(age, gender):
    try:
        # 1. age 반올림
        age = round(age, -1)
        
        # 2. 버킷 연결
        storage = minio_connection()
        
        # 3. 버킷에서 리스트 가져오기 
        ret = minio_list_object(storage, age, gender)

        # 4. 버킷에서 리스트 가져오기 성공 시 랜덤 선정 
        if ret == False:
            return False, {"error":"Can't find list"} #false ->400 
        else:
            print(ret)
            choicejpg = random.choice(ret)
            idx = choicejpg.rindex('.')
            choicemp4 = choicejpg[:idx] + '.mp4'
            return True, {"image" : choicejpg, "gif" : choicemp4}
        
    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        return False, {"error" : str(ex)}  #false -> 400