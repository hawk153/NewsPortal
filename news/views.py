from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .filters import FilterNews
from .forms import CreateForm
from .models import Post



class NewsList(ListView):
    model = Post
    ordering = '-post_creation_date'
    template_name = 'allnews.html'
    context_object_name = 'allnews'
    paginate_by = 10


class SearchNews(ListView):
    model = Post
    ordering = '-post_creation_date'
    template_name = 'searchnews.html'
    context_object_name = 'selectednews'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = FilterNews(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class DefiniteNews(DetailView):
    model = Post
    template_name = 'definitenews.html'
    context_object_name = 'definitenews'


class CreateNews(PermissionRequiredMixin, CreateView):
    form_class = CreateForm
    model = Post
    template_name = 'createnews.html'
    permission_required = ('news.add_post', )
    raise_exception = True


class UpdateNews(PermissionRequiredMixin, UpdateView):
    form_class = CreateForm
    model = Post
    template_name = 'updatenews.html'
    permission_required = ('news.change_post', )
    raise_exception = True


class ErasingNews(PermissionRequiredMixin,DeleteView):
    model = Post
    template_name = 'deletenews.html'
    success_url = reverse_lazy('allnews')
    permission_required = ('news.delete_post',)
    raise_exception = True