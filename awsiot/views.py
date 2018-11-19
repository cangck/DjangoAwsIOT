import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
# Create your views here.
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from awsiot.thirdSdk.mobsmssdk import MobSMS, MOB_KEY, MobStatus


def result(code, data):
    return '{' + "code:" + str(code) + '\",{' + "data:" + json.dumps(data) + '}' + '}'


def index(request):
    return Response("hello")


class UserViewSet(APIView):

    def get(self, request):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


# class UserRegister(APIView):
#     '''
#        用户登录信息处理流程
#        '''
#     # 设置当前的View不需要认证权限
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = RegisterSerializer
#
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         # 验证用户名密码不正确
#         if not serializer.is_valid():
#             return Response({
#                 'code': status.HTTP_400_BAD_REQUEST,
#                 'data': serializer.data,
#                 'extrs': serializer.errors['username']
#             }, content_type='application/json')
#         code = request.data["code"];
#         mobsms = MobSMS('28d339dc325c0')
#         result_code = mobsms.verify_sms_code(86, 15112286305, '6825', debug=False)
#         # 请求成功,保存进入数据库
#         if result_code == MobStatus.MOBSTATUS_SUCCESS:
#             serializer.save()
#             return Response({
#                 'code': status.HTTP_200_OK,
#                 'data': serializer.validated_data,
#                 'extrs': []
#             }, content_type='application/json')
#         else:
#             # 验证码不对
#             return Response({
#                 'code': status.HTTP_200_OK,
#                 'data': serializer.validated_data,
#                 'extrs': []
#             }, content_type='application/json')


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
                    result_code = mobsms.verify_sms_code("86", phone=phone, code=code, debug=False)
                    print(str(result_code))
                    result_code = 200
                    if result_code == MobStatus.MOBSTATUS_SUCCESS:
                        user = User.objects.create()
                        user.username = username
                        user.password = make_password(password, salt='pbkdf2_sha256')
                        user.save()
                        return Response({
                            'code': result_code,
                            'data': "",
                            'msg': "用户注册成功"
                        }, content_type='application/json')
                    else:
                        return Response({
                            'code': result_code,
                            'data': "",
                            'msg': "验证码错误"
                        }, content_type='application/json')

                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'data': str(request.data),
                    'msg': "当前用户已存在!!!"
                }, content_type='application/json')

            elif path_info == "/login/":
                return Response(path_info)
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
