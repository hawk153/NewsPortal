from datetime import datetime

from django.views.generic import ListView, DetailView

from .models import Post


# Create your views here.
class NewsList(ListView):
    model = Post
    ordering = '-post_creation_date'
    template_name = 'allnews.html'
    context_object_name = 'allnews'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        return context


class DefiniteNews(DetailView):
    model = Post
    template_name = 'definitenews.html'
    context_object_name = 'definitenews'

# Create your views here.
