from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.serializers import RefreshJSONWebTokenSerializer
from rest_framework_jwt.views import VerifyJSONWebToken, RefreshJSONWebToken, ObtainJSONWebToken

from AwsIotWeb import settings


class CustomeRefreshJSONWebTokenSerializer(RefreshJSONWebTokenSerializer):
    pass


class CustomObtainJSONWebToken(ObtainJSONWebToken):
    '''
    定制获取Token的返回值
    '''

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            return Response({
                'code': status.HTTP_200_OK,
                'time': timezone.now(),
                'expire': settings.JWT_AUTH['JWT_EXPIRATION_DELTA'],
                'token': token
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomVerifyJSONWebToken(VerifyJSONWebToken):
    pass


class CustomRefreshJSONWebToken(RefreshJSONWebToken):
    serializer_class = CustomeRefreshJSONWebTokenSerializer
