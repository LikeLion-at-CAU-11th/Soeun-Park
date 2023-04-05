from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Post

# View == Controller와 비슷한 역할 


#### week 4 ####
# 스탠다드 과제 
@require_http_methods(["GET"])
def get_post_detail(request, id):
    post = get_object_or_404(Post, pk = id) # object를 가져오거나 or 404를 띄운다
    category_json = {
        "id": post.post_id,
        "writer": post.writer,
        "content": post.content,
        "category": post.category,
    }
    
    # JsonResponse는 HttpResponse를 상속받은 클래스 
    return JsonResponse({
        'status': 200,
        'message': '게시글 조회 성공',
        'data': category_json
    })

# 챌린지 과제 
@require_http_methods(["GET"])
def get_posts(request):
    posts = Post.objects.all()
    postList = []
    
    for post in posts:
        postList.append({
            "id": post.post_id,
            "writer": post.writer,
            "content": post.content,
            "category": post.category,
        })
    
    return JsonResponse({
        'status': 200,
        'message': '게시글 리스트 조회 성공',
        'data': postList
    })


#### week 3 ####
# 스탠다드 과제 
def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status': 200,
            'success': True,
            'message': '메시지 전달 성공~',
            'data': 'Hello World',
        })

# 챌린지 과제
def challenge(request):
    if request.method == "GET":
        return JsonResponse({
            'status': 200,
            'success': True,
            'message': '메시지 전달 성공~~',
            'data': [
                {
                    "name": "박소은",
                    "age": 23,
                    "major": "소프트",
                },
                {
                    "name": "이기웅",
                    "age": 24,
                    "major": "에너지시스템공학부"
                }
            ]
        })