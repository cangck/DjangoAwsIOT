import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
# Create your views here.
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView

from AwsIotWeb import settings
from awsiot.thirdSdk.mobsmssdk import MobSMS, MOB_KEY, MobStatus


def resultJson(code, data, msg):
    return Response({
        'code': code,
        'data': data,
        'msg': msg
    }, content_type='application/json')


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

    def post(self, request):
        try:
            # print(request.META)
            path_info = request.META['PATH_INFO']
            username = request.data['username']
            password = request.data['password']
            if path_info == "/register/":
                code = request.data['code']
                phone = request.data['phone']
                zone = request.data['zone']
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    mobsms = MobSMS(MOB_KEY)
                    # 第三方服务器验证短信登录信息
                    result_code = mobsms.verify_sms_code("86", phone=phone, code=code, debug=False)
                    result_code = 200
                    if result_code == MobStatus.MOBSTATUS_SUCCESS:
                        user = User.objects.create()
                        user.username = username
                        user.password = make_password(password, salt='pbkdf2_sha256')
                        user.save()
                        return resultJson(status.HTTP_200_OK, "", "用户注册成功")
                    else:
                        return resultJson(result_code, "", "验证码错误")
                return resultJson(status.HTTP_400_BAD_REQUEST, str(request.data), "当前用户已经存在！！！")

            elif path_info == "/login/":
                username = request.data['username']
                password = request.data['password']

                try:
                    user = User.objects.get(username=username)
                    if user.password == make_password(password, salt='pbkdf2_sha256'):
                        # 生成一个token给登录的用户
                        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                        payload = jwt_payload_handler(user)
                        token = jwt_encode_handler(payload)
                        strtoken = {
                            'code': status.HTTP_200_OK,
                            'time': timezone.now(),
                            'expire': settings.JWT_AUTH['JWT_EXPIRATION_DELTA'],
                            'token': token
                        }
                        return resultJson(status.HTTP_200_OK, strtoken, "登录成功!!!")
                    else:
                        return resultJson(status.HTTP_401_UNAUTHORIZED, "", "密码错误")

                except User.DoesNotExist:
                    return resultJson(status.HTTP_401_UNAUTHORIZED, str(request.data), "密码错误")
        except Exception as es:
            return Response(es)


class TestView(APIView):
    # 设置当前的View不需要认证权限
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        path_info = request.META['PATH_INFO']
        if path_info == '/test/':
            return Response('test/')
        elif path_info == "/test1/":
            return Response('test1')
        print(request.META)
