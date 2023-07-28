from rest_framework import serializers
from .models import Post    # 현재 디렉토리(.)의 models 파일의 Post class
from .models import Comment
from config import settings
import boto3
from botocore.exceptions import ClientError

# 유효한 이미지 파일인지 검사
def is_image(image):
    file_extensions = ['jpg', 'jpeg', 'png', 'gif']
    file_extension = image.name.split('.')[-1].lower()  # 이미지의 확장자
    
    if file_extension not in file_extensions:
        return False
    return True


class PostSerializer(serializers.ModelSerializer):  # ModelSerializer 상속
    class Meta:
        model = Post    # 어떤 모델을 serialize할 것인지
        fields = "__all__"  # 모든 필드를 가져오기
    
    # validate image
    def validate(self, data):
        image = data.get('thumbnail')
        if not is_image(image):
            raise serializers.ValidationError('Not an image file')
        else:
            s3_url = self.save_image(image)
            if not s3_url:
                raise serializers.ValidationError('Invalid image file')
            data['thumbnail'] = s3_url
        return data
    
    def save_image(self, image):
        try:
            # s3 client 생성
            s3 = boto3.client('s3',
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                            region_name=settings.AWS_REGION)

            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            file_path = image.name
            s3.upload_fileobj(image, bucket_name, file_path)    # s3에 업로드
            
            s3_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_path}"
            return s3_url
        except:
            print("s3 upload error")
            return None

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"