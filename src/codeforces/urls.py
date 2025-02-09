from django.urls import path
from . import views

urlpatterns = [
    path('participants/<str:username>', views.codeforces_user_info, name='codeforces_user_info'),
    path('participants/', views.participants, name = 'participants')
]
