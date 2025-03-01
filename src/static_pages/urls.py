from django.urls import path
from .views import StaticPageDetailView, HomeTemplateView

urlpatterns = [
    path('home/', HomeTemplateView.as_view(), name='home_template'),
    path('<slug:slug>/', StaticPageDetailView.as_view(), name='static_page_detail'),
]
