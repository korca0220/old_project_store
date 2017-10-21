from storages.backends.s3boto3 import S3Boto3Storage

#각각 static, media 별로 따로 저장하기 위함
# 아래 설정을 하지않으면 같은 공간에 저장이 됨

class StaticS3Boto3Storage(S3Boto3Storage):
    location = 'static' # bucket 업로드 prefix 지정

class MediaS3Boto3Storage(S3Boto3Storage):
    location = 'media' # bucket 업로드 prefix 지정
