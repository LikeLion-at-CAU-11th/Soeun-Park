from django.urls import path
from posts.views import *

urlpatterns = [
    # path('', hello_world, name='hello_world'),
    # path('introduction/', challenge, name='assignment_challenge'),
    path('<int:id>/', get_post_detail, name="get_post_detail"),
    path('', get_posts, name="get_posts")
]
