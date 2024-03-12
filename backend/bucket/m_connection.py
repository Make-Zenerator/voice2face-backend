from minio import Minio
from bucket.m_config import ACCESS_KEY, SECRET_KEY
from bucket.m_config import BUCKET_NAME, MINIO_API_HOST

def minio_connection():
    try:
        print(MINIO_API_HOST)
        print(ACCESS_KEY)
        print(SECRET_KEY)
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

# def s3_get_object(s3, bucket, object_name, file_name):
#     '''
#     s3 bucket에서 지정 파일 다운로드
#     :param s3: 연결된 s3 객체(boto3 client)
#     :param bucket: 버킷명
#     :param object_name: s3에 저장된 object 명
#     :param file_name: 저장할 파일 명(path)
#     :return: 성공 시 True, 실패 시 False 반환
#     '''
#     try:
#         s3.download_file(bucket, object_name, file_name)
#     except Exception as e:
#         print(e)
#         return False
#     return True