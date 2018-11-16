from django.contrib.auth.models import User, Group
from django.http.response import HttpResponse


# Create your views here.
from rest_framework import viewsets

from awsiot.serializer.serializer import UserSerializer, GroupSerializer


def index(request):
    return HttpResponse("AwsIotWeb");


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer