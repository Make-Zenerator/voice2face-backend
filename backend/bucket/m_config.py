from dotenv import load_dotenv
import os

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET_REGION = os.getenv('AWS_S3_BUCKET_REGION')
AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
AWS_S3_BUCKET_URL = os.getenv('AWS_S3_BUCKET_URL')