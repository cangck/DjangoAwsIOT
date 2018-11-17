import json

from django.contrib.auth.models import User
# Create your views here.
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

import time

from awsiot.serializer.serializer import RegisterSerializer


def result(code, data):
    return '{' + "code:" + str(code) + '\",{' + "data:" + json.dumps(data) + '}' + '}'


def index(request):
    return Response("hello")


class UserViewSet(APIView):

    def get(self, request):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


class UserRegister(APIView):
    '''
       用户登录信息处理流程
       '''
    # 设置当前的View不需要认证权限
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'data': serializer.data,
                'extrs': serializer.errors['username']
            }, content_type='application/json')
        serializer.save()
        return Response({
            'code': status.HTTP_200_OK,
            'data': serializer.validated_data,
            'extrs': ""
        }, content_type='application/json')
