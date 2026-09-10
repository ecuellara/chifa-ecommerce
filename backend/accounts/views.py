from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, MeSerializer, EmailOrUsernameTokenObtainPairSerializer


class AuthBurstThrottle(AnonRateThrottle):
    scope = 'auth_burst'


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AuthBurstThrottle]
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
        user = s.save()
        return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)

class CustomLoginView(TokenObtainPairView):
    serializer_class = EmailOrUsernameTokenObtainPairSerializer
    throttle_classes = [AuthBurstThrottle]

class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(MeSerializer(request.user).data)