# django
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Post, Comment
import json
from datetime import datetime, timedelta
# DRF
from .serializers import PostSerializer
from .serializers import CommentSerializer
# APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# DRF 사용: 게시글 리스트
class PostList(APIView):
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        posts = Post.objects.all()  # queryset으로 받아오기
        serializer = PostSerializer(posts, many=True)   # 많은 값을 받을 때는 many=True
        return Response(serializer.data)

# DRF 사용: 게시글 단일 객체
class PostDetail(APIView):
    def get(self, request, id):
        post = get_object_or_404(Post, post_id=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, id): # 모두 수정
        post = get_object_or_404(Post, post_id=id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        post = get_object_or_404(Post, post_id=id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# DRF 사용: 댓글
class PostComment(APIView):
    def get(self, request, id):
        comments = Comment.objects.filter(post=id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Mixins 사용
from rest_framework import mixins
from rest_framework import generics

class PostListMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class PostDetailMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Concrete Generic Views 사용
class PostListGenericAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# ViewSet 사용
from rest_framework import viewsets

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

'''
# DefaultRouter가 알아서 해주기 때문에 없어도 됨
post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})
'''




'''
# Django 사용
####    모든 posts 조회하기   ####
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


####    특정 기간에 생성된 post 조회하기(w5 챌린지 과제)    ####
@require_http_methods(["GET"])
def get_posts_datetime(request):
    start_date_str = request.GET['from']
    end_date_str = request.GET['to']
    
    # string -> datetime으로 타입 바꿔주기
    start_datetime = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(hours=23, minutes=59, seconds=59)    # 마지막날 23시 59분까지
    
    posts = Post.objects.filter(created_at__range=(start_datetime, end_datetime))
    
    posts_json_list = []
    for post in posts:
        posts_json_list.append({
            "id": post.post_id,
            "writer": post.writer,
            "content": post.content,
            "category": post.category,
            "created_at": post.created_at,   # 시간 확인 차 넣어줌
        })
    
    return JsonResponse({
        'status': 200,
        'message': '특정 기간에 작성된 게시글 조회 성공',
        'data': posts_json_list
    })


####    post_detail 조회하기/수정하기/삭제하기  ####
@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, id):
    if request.method == "GET":
        post = get_object_or_404(Post, pk = id) # object를 가져오거나 or 404를 띄운다(queryset 형태)
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


####    댓글 생성하기/조회하기  ####
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
'''


'''
#### week 3 ####
스탠다드 과제 
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
'''