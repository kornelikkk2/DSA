from django.urls import path
from . import views
 
urlpatterns = [
    path('api/qr_codes/', views.receive_qr_data, name='receive_qr_data'),
] 