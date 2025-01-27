from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>', views.codeforces_user_info, name='codeforces_user_info')
]
