from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterApiView, LoginView, LogoutView, HomePage

router = DefaultRouter()

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('home/', HomePage.as_view(), name='home'),

    path('login/', LoginView.as_view(), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),

]
