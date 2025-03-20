from django.urls import path
from .views import SectionDetailView, PageDetailView, SectionListView

urlpatterns = [
    path('sections/', SectionListView.as_view(), name='section_list'),
    path('<slug:slug>/', SectionDetailView.as_view(), name='section_detail'),
    path('page/<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
]
