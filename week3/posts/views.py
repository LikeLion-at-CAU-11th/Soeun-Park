from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status': 200,
            'success': True,
            'message': '메시지 전달 성공~',
            'data': 'Hello World',
        })
        
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