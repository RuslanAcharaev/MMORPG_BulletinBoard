from django.urls import path
from .views import AdsList, AdDetail, AdCreate, AdUpdate, AdDelete, ResponseCreate, response_list, response_accept, \
    ResponseDelete, forbidden

urlpatterns = [
    path('', AdsList.as_view(), name='ad_list'),
    path('<int:pk>', AdDetail.as_view(), name='ad_detail'),
    path('create/', AdCreate.as_view(), name='ad_create'),
    path('<int:pk>/edit', AdUpdate.as_view(), name='ad_update'),
    path('<int:pk>/delete', AdDelete.as_view(), name='ad_delete'),
    path('<int:pk>/response/create', ResponseCreate.as_view(), name='response_create'),
    path('responses/', response_list, name='response_list'),
    path('responses/<int:response_id>/accept', response_accept, name='response_accept'),
    path('responses/<int:pk>/delete', ResponseDelete.as_view(), name='response_delete'),
    path('forbidden/', forbidden, name='forbidden')
]
