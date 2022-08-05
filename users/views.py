from rest_framework import views, response, permissions
from django.contrib.auth import login, logout
from .authentication import CsrfExemptSessionAuthentication
from .serializers import LoginSerializer, UserSerializer

from django.contrib.auth.models import User


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return response.Response(UserSerializer(user).data)


class LogoutView(views.APIView):
    authentication_classes = [CsrfExemptSessionAuthentication, ]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        logout(request)
        return response.Response()


class SessionUserView(views.APIView):

    def get(self, request):
        user = User.objects.get(pk=self.request.user.id)
        serializer = UserSerializer(user)
        return response.Response(data=serializer.data)
