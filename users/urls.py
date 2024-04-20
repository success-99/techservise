from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterApiView, LoginApiView, LogoutApiView, HomePage, RegisterApiViewList

router = DefaultRouter()
router.register('register', RegisterApiView, basename='register')

urlpatterns = [
    # path('register/', RegisterApiView.as_view(), name='register'),
    path('home/', HomePage.as_view(), name='home'),
    # path('token-auth/', CustomAuthToken.as_view()),

    path('user-list/', RegisterApiViewList.as_view(), name='list'),

    path('login/', LoginApiView.as_view(), name='login'),

    path('logout/', LogoutApiView.as_view(), name='logout'),
    path('', include(router.urls)),

]

