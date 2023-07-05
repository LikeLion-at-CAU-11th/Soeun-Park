from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import Member

# 회원가입
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    
    class Meta:
        model = Member
        fields = ['id', 'password', 'username', 'email', 'age']
    
    
    # 회원정보 저장
    def save(self, request):
        member = Member.objects.create(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            age=self.validated_data['age'],
        )
		
        member.set_password(self.validated_data['password'])    # password 암호화
        member.save()
        return member
    
    
    # email이나 username이 겹치지 않도록 검증
    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)

        if Member.objects.filter(email=email).exists():
            raise serializers.ValidationError('email already exists')
        
        if Member.objects.filter(username=username).exists():
            raise serializers.ValidationError('username already exists')
        
        return data


# 로그인/로그아웃
class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = Member
        fields = ['username', 'password']
    
    
    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
				
		# Member DB에서 요청의 username과 일치하는 데이터가 존재하는지 확인
        if Member.objects.filter(username=username).exists():
            member = Member.objects.get(username=username)

            # DB에 해당 데이터가 존재하는데 password가 일치하지 않는 경우
            if not member.check_password(password):
                raise serializers.ValidationError("wrong password")
        else:
            raise serializers.ValidationError("member account not exist")
        
        
        # user가 맞는 경우 토큰 발급해준다
        token = RefreshToken.for_user(member)
        refresh_token = str(token)
        access_token = str(token.access_token)
        data = {
			'member':member,
			'refresh_token':refresh_token,
			'access_token':access_token,
		}
        
        return data