from minio import Minio
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

def minio_list_object(storage, age, gender):
    '''
    minio bucket에서 해당 성별과 나이에 맞는 이미지 리스트 가져오기
    :param storage: 연결된 minio 객체(Minio client)
    :param prefix: Object name starts with prefix.
    :param age: 나이
    :param gender: 성별
    :return: 성공 시 list 반환, 실패 시 False 반환
    '''
    try:
        prefix = "output_condition/"
        obj_list = list(storage.list_objects(BUCKET_NAME, prefix))
        contents_list = [obj.object_name for obj in obj_list]
        print(contents_list)
        
        file_list = [content['Key'] for content in contents_list]
        print(type(file_list))
        condition_file_list = []
        for file in file_list:
            print(type(file))
            _, file_name = file.split('-')
            idx = file_name.rindex('.')
            print(file_name)
            print(idx)
            if file_name[idx+1:] == 'jpg' and file_name[:idx] == f'{gender}_{age}':
                condition_file_list.append(file)
    except Exception as e:
        print(e)
        return False
    return condition_file_list

def read_random_condition(age, gender):
    try:
        # 1. age 반올림
        age = round(int(age), -1)
        
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