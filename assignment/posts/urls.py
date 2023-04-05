from django.urls import path
from posts.views import *

urlpatterns = [
    # 3주차 과제
    # path('', hello_world, name='hello_world'),
    # path('introduction/', challenge, name='assignment_challenge'),
    
    # post
    path('', get_all_posts, name="get_all_posts"),
    path('new-post', create_post, name="create_post"),
    path('<int:id>', post_detail, name="post_detail"),
    
    # comment
    path('<int:post_id>/comment', comment, name='comment'),
]
