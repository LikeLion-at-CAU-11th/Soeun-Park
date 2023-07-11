from django.urls import path, include
from posts.views import *
from . import views
from rest_framework.routers import DefaultRouter

# Router 설정
# router = DefaultRouter()
# router.register('', PostViewSet)    # post 관련 api
# router.register('<int:pk>/comment', CommentViewSet)
# router.register('(?P<bk>[^/.]+)/comment', CommentViewSet)   # comment 관련 api(정규표현식 사용)

# ViewSet 사용
urlpatterns = [
    path('', PostList.as_view()),
    path('<int:id>/', PostDetail.as_view())
]

'''
# Concrete Generic Views 사용
urlpatterns = [
    path('', PostListGenericAPIView.as_view()),
    path('<int:pk>/', PostDetailGenericAPIView.as_view()),
]
'''

'''
# Mixins 사용
urlpatterns = [
    path('', PostListMixins.as_view()),
    path('<int:pk>/', PostDetailMixins.as_view()),
]
'''

'''
# DRF 사용
urlpatterns = [
    # DRF urls
    path('', PostList.as_view()),
    path('<int:id>/', PostDetail.as_view()),
    path('<int:id>/comment', PostComment.as_view())
]
'''

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