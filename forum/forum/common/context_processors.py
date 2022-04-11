from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from forum.main.models import Category, Post


def categories(request):
    categories = Category.objects.all()
    return {'categories': categories}


def search(request):
    q = request.GET.get('q')
    if q:
        vector = SearchVector('title') + SearchVector('category__title') \
                 + SearchVector(StringAgg('tag__name', delimiter=' '))
        query = SearchQuery(q)

        posts = Post.objects.annotate(rank=SearchRank(vector, query))\
            .filter(rank__gte=0.0001).order_by('-rank').distinct()
    else:
        posts = None

    context = {'posts': posts}
    return context

