from django.views.generic import DetailView, ListView
from .models import Section, Page


class SectionDetailView(DetailView):
    model = Section
    template_name = 'handbook/section_detail.html'
    context_object_name = 'section'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subsections'] = Section.objects.filter(parent=self.object, is_hidden=False)
        context['pages'] = Page.objects.filter(sections=self.object, is_hidden=False)

        return context


class PageDetailView(DetailView):
    model = Page
    template_name = 'handbook/page_detail.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Page.objects.filter(is_hidden=False)


class SectionListView(ListView):
    model = Section
    template_name = 'handbook/section_list.html'
    context_object_name = 'sections'

    def get_queryset(self):
        return Section.objects.filter(is_hidden=False, parent__isnull=True)
