import django_filters
from django.contrib.auth.models import User
from rest_framework import exceptions, generics, permissions, viewsets, mixins, status
from rest_framework.decorators import api_view, permission_classes, list_route
from rest_framework.response import Response

from . import models, serializers


class CreateUserView(generics.CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserSerializer

class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    list:
    Return a list of all the existing users.
    read:
    Return the given user.
    me:
    Return authenticated user.
    change password:
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    # permission_classes = (IsSuperuserOrIsSelf,)
    @list_route(methods=['get'], serializer_class=serializers.UserSerializer,  url_path='me')
    def me(self, request):            
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)


    @list_route(methods=['put'], serializer_class=serializers.PasswordChangeSerializer,  url_path='change-password')
    def set_password(self, request):
        serializer = serializers.PasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            if not request.user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong password.']}, 
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            request.user.set_password(serializer.data.get('new_password'))
            request.user.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)     

