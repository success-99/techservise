from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from users.models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'msg': 'success register'}, status=201)


class LoginView(APIView):
    # permission_classes = [IsAuthenticated]  # Kimdir kirishi mumkin
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = CustomUser.objects.filter(email=email).first()
        token, created = Token.objects.get_or_create(user=user)
        response_data = {'token': token.key}
        if created:
            response_data['message'] = 'Foydalanuvchi muvaffaqiyatli login qildi.'
        else:
            response_data['message'] = 'Foydalanuvchi allaqachon tizimga kirdi.'
        return Response(response_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            request.user.auth_token.delete()
            return Response({'detail': 'Foydalanuvchi sessiyasidan muvaffaqiyatli chiqarildi.'},
                            status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Foydalanuvchi uchun token topilmadi. Foydalanuvchi allaqachon chiqib ketgan.'},
                            status=status.HTTP_400_BAD_REQUEST)


class HomePage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            return Response(data={'msg': "Siz ro'yxatdan o'tgansiz!"}, status=200)
        return Response(data={'msg': "Xatolik! ro'yxatdan o'ting!"}, status=400)