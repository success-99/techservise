from django.urls import path, include
from .views import GenerateContracts, DownloadOutputView

urlpatterns = [
    path('excel_to_word/', GenerateContracts.as_view(), name='excel_to_word'),
    path('dow_word/', DownloadOutputView.as_view(), name='dow_word'),

]
