from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from apps.users.models import User
from apps.users.serializers.user_serializers import RegisterUserSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Убедитесь, что это разрешает доступ для анонимных пользователей
