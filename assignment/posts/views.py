from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Post, Comment
import json


####    모든 posts 가져오기   ####
@require_http_methods(["GET"])
def get_all_posts(request):
    posts = Post.objects.all()
    post_json_list = []
    
    for post in posts:
        post_json_list.append({
            "id": post.post_id,
            "writer": post.writer,
            "content": post.content,
            "category": post.category,
        })
    
    return JsonResponse({
        'status': 200,
        'message': '게시글 리스트 조회 성공',
        'data': post_json_list
    })


####    새로운 post 생성하기   ####
@require_http_methods(["POST"])
def create_post(request):
    body = json.loads(request.body.decode('utf-8')) # decoding 과정
    
    # ORM을 통하여 새로운 데이터를 DB에 저장한다
    new_post = Post.objects.create(
        writer = body['writer'],
        content = body['content'],
        category = body['category']
    )
    
    # DB에서 확인하기 번거로우니 Json 형식에 넣어서 반환해주자
    new_post_json = {
        "post_id": new_post.post_id,
        "writer": new_post.writer,
        "content": new_post.content,
        "category": new_post.category,
    }
    
    return JsonResponse({
        'status': 200,
        'message': '게시글 생성 성공',
        'data': new_post_json
    })


####    post_detail 가져오기/수정하기/삭제하기  ####
@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, id):
    if request.method == "GET":
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
    
    elif request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        update_post = get_object_or_404(Post, pk=id)    # 저장한 데이터를 DB에서 가져온다
        
        # post_id, writer는 바뀌지 않는 필드이므로 수정 X
        update_post.content = body['content']
        update_post.category = body['category']
        update_post.save()  # 변동 사항을 DB에 저장
        
        # 변동사항이 잘 적용되었는지 Json 형식으로 확인
        update_post_json = {
            "id": update_post.post_id,
            "writer": update_post.writer,
            "content": update_post.content,
            "category": update_post.category
        }
        
        return JsonResponse({
            'status': 200,
            'message': '게시글 수정 성공',
            'data': update_post_json
        })
    
    elif request.method == "DELETE":
        delete_post = get_object_or_404(Post, pk=id)
        delete_post.delete()
        
        return JsonResponse({
            'status': 200,
            'message': '게시글 삭제 성공',
            'data': None,
        })


####    댓글 생성하기/가져오기  ####
@require_http_methods(["GET", "POST"])
def comment(request, post_id):
    if request.method == "GET":
        comments = Comment.objects.filter(post=post_id) # Comment의 post == Post의 post_id
        
        comment_json_list = []
        for comment in comments:
            comment_json = {
                'writer': comment.writer,
                'content': comment.content
                # id는 굳이 가져올 필요 없다~
            }
            comment_json_list.append(comment_json)
            
        return JsonResponse({
            'status': 200,
            'message': '댓글 읽어오기 성공',
            'data': comment_json_list
        })
    
    elif request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        
        new_comment = Comment.objects.create(
            writer = body['writer'],
            content = body['content'],
            post = Post.objects.get(pk=post_id)
        )
        
        new_comment_json = {
            'writer': new_comment.writer,
            'content': new_comment.content,
            'post_id': new_comment.post.post_id # 확인용으로 post_id도 넣어주었다 
        }
        
        return JsonResponse({
            'status': 200,
            'message': '댓글 생성 성공',
            'data': new_comment_json
        })




#### week 3 ####
# 스탠다드 과제 
# def hello_world(request):
#     if request.method == "GET":
#         return JsonResponse({
#             'status': 200,
#             'success': True,
#             'message': '메시지 전달 성공~',
#             'data': 'Hello World',
#         })

# # 챌린지 과제
# def challenge(request):
#     if request.method == "GET":
#         return JsonResponse({
#             'status': 200,
#             'success': True,
#             'message': '메시지 전달 성공~~',
#             'data': [
#                 {
#                     "name": "박소은",
#                     "age": 23,
#                     "major": "소프트",
#                 },
#                 {
#                     "name": "이기웅",
#                     "age": 24,
#                     "major": "에너지시스템공학부"
#                 }
#             ]
#         })