from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.core.paginator import Paginator

from forum.main.models import Category, Post


def categories(request):
    categories = Category.objects.all()
    return {'categories': categories}


def search(request):
    q = request.GET.get('q')
    if q:
        vector = SearchVector('title')
        query = SearchQuery(q)
        search_headline = SearchHeadline('title', query)

        posts = Post.objects.annotate(rank=SearchRank(vector, query)).annotate(headline=search_headline)\
            .filter(rank__gte=0.001).order_by('-rank')
    else:
        posts = None

    context = {'posts': posts}
    return context

