from django.urls import path
from posts.views import *

urlpatterns = [
    # DRF urls
    path('', PostList.as_view()),
    path('<int:id>/', PostDetail.as_view()),
    path('<int:id>/comment', PostComment.as_view())
]

'''
    # django
    # 3주차 과제
    # path('', hello_world, name='hello_world'),
    # path('introduction/', challenge, name='assignment_challenge'),
    
    # post
    path('', get_all_posts, name="get_all_posts"),
    path('new-post', create_post, name="create_post"),
    path('<int:id>', post_detail, name="post_detail"),
    path('date', get_posts_datetime, name="get_posts_datetime"),
    
    # comment
    path('<int:post_id>/comment', comment, name='comment'),
    '''