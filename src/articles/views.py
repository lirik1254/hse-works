from django.views.generic import ListView, DetailView

from articles.models import Article, ArticleTag, ArticleComment


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 20

    def get_queryset(self):
        queryset = Article.objects.filter(is_hidden=False).order_by('-created_at')
        query = self.request.GET.get('q', '')
        author_id = self.request.GET.get('author')
        tag_id = self.request.GET.get('tag')

        if query:
            queryset = queryset.filter(title__icontains=query)

        if author_id:
            queryset = queryset.filter(author_id=author_id)

        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['author_id'] = self.request.GET.get('author', '')
        context['tag_id'] = self.request.GET.get('tag', '')
        context['tags'] = ArticleTag.objects.all()

        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.filter(is_hidden=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = (ArticleComment.objects.filter(article=self.object, is_hidden=False)
                               .order_by('-created_at'))

        return context
