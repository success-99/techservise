from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics, permissions, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


# class CustomAuthToken(ObtainAuthToken):
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })


class RegisterApiView(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterApiViewList(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = RegisterSerializer


class LoginApiView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Ma'lumotlarni olish
            email = serializer.validated_data.get('email')

            if email:
                user = CustomUser.objects.filter(email=email).first()
                if user:
                    token, created = Token.objects.get_or_create(user=user)
                    response_data = {'token': token.key, 'id': user.id}
                    if created:
                        response_data['message'] = 'Foydalanuvchi muvaffaqiyatli login qildi.'
                    else:
                        response_data['message'] = 'Foydalanuvchi allaqachon tizimga kirgan.'
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Foydalanuvchi topilmadi.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Email kiritilmadi.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(generics.DestroyAPIView):
    # serializer_class = LoginSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:  # Foydalanuvchi autentifikatsiyadan o'tkazilganligini tekshirish
                request.user.auth_token.delete()
                return Response({'detail': 'Foydalanuvchi muvaffaqiyatli logout qildi.'}, status=status.HTTP_200_OK)
            else:
                return Response({
                                    'detail': "Foydalanuvchi avtorizatsiyadan o'tkazilmaganligi sababli sessiyadan chiqarish mumkin emas."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class HomePage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            return Response(data={'msg': "Siz ro'yxatdan o'tgansiz!"}, status=200)
        return Response(data={'msg': "Xatolik! ro'yxatdan o'ting!"}, status=400)
