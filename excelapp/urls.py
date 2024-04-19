from django.urls import path, include
from .views import GenerateContracts

urlpatterns = [
    path('excel_to_word/', GenerateContracts.as_view(), name='excel_to_word'),

]
