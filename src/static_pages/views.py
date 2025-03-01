from django.views.generic import DetailView, TemplateView

from static_pages.models import StaticPage


class StaticPageDetailView(DetailView):
    model = StaticPage
    template_name = 'static_pages/static_page_detail.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return StaticPage.objects.filter(is_hidden=False)


class HomeTemplateView(TemplateView):
    template_name = 'static_pages/home_template.html'
