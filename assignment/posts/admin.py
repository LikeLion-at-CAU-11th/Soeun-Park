from django.contrib import admin
from .models import Post, Comment

admin.site.register(Post)   # 테이블 당 하나씩 register
admin.site.register(Comment)