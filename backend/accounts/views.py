from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
        user = s.save()
        return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)