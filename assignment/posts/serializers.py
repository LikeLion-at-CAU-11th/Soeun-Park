from rest_framework import serializers
from .models import Post    # 현재 디렉토리(.)의 models 파일의 Post class
from .models import Comment

class PostSerializer(serializers.ModelSerializer):  # ModelSerializer 상속
    class Meta:
        model = Post    # 어떤 모델을 serialize할 것인지
        fields = "__all__"  # 모든 필드를 가져오기
        
        # fields = ['writer', 'content']    # 일부 필드만 가져오기
        # exclude = ["id"]      # 제외할 필드 지정
        # read_only_fields = ['writer']     # read만 되는 필드 선언

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"