from django.urls import path
from .views import AdsList, AdDetail, AdCreate, AdUpdate, AdDelete, ResponseCreate

urlpatterns = [
    path('', AdsList.as_view(), name='ad_list'),
    path('<int:pk>', AdDetail.as_view(), name='ad_detail'),
    path('create/', AdCreate.as_view(), name='ad_create'),
    path('<int:pk>/edit', AdUpdate.as_view(), name='ad_update'),
    path('<int:pk>/delete', AdDelete.as_view(), name='ad_delete'),
    path('<int:pk>/response/create', ResponseCreate.as_view(), name='response_create'),
]
