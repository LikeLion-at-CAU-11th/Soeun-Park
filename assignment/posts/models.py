from django.db import models

# BaseModel 클래스: 공통으로 사용할 속성, 기능을 정의한 class
class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)   # auto_now_add: 최초 저장할 때의 날짜 적용(갱신 불가능)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)   # auto_now: 모델이 저장될 때마다 저장 날짜 적용(갱신 가능)
    # verbose_name: admin에서 볼 때의 이름

    class Meta:
        abstract = True # BaseModel을 상속 가능하도록

class Post(BaseModel):  # BaseMode 클래스를 상속

    CHOICES = (
        ('DIARY', '일기'),
        ('STUDY', '공부'),
        ('ETC', '기타')
    )

    post_id = models.AutoField(primary_key=True)
    writer = models.CharField(verbose_name="작성자", max_length=30)
    content = models.TextField(verbose_name="내용")
    category = models.CharField(choices=CHOICES, max_length=20)
    # choices: dropbox


class Comment(BaseModel):
    writer = models.CharField(verbose_name="작성자", max_length=30)
    content = models.CharField(verbose_name="내용", max_length=200)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, blank=False)    # Post를 참조(일대다 관계)
    # CASCADE: post가 삭제되었을 때 comment도 삭제됨