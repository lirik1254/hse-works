from django.views.generic import ListView, DetailView

from news.models import News, NewsCategory, NewsComment


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 1

    def get_queryset(self):
        queryset = News.objects.filter(is_hidden=False).order_by('-created_at')
        query = self.request.GET.get('q', '')
        author_id = self.request.GET.get('author')
        category_id = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(title__icontains=query)

        if author_id:
            queryset = queryset.filter(author_id=author_id)

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['author_id'] = self.request.GET.get('author', '')
        context['category_id'] = self.request.GET.get('category', '')
        context['categories'] = NewsCategory.objects.all()

        return context


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.filter(is_hidden=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = (NewsComment.objects.filter(news=self.object, is_hidden=False)
                               .order_by('-created_at'))

        return context
