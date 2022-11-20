from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission, User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .filters import FilterNews
from .forms import CreateForm
from .models import Post, Author, Category
from .tasks import announce


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
    permission_required = ('news.add_post',)
    raise_exception = True

    # success_url = reverse_lazy('news-created')

    def form_valid(self, form):
        print(form)
        time_now = datetime.now()
        time_day_ago = time_now - timedelta(hours=24)
        post_list = Post.objects.filter(Q(post_creation_date__gte=time_day_ago) & Q(
            author_name=form.instance.author_name))
        if len(post_list) <= 3:
            return super().form_valid(form)
        else:
            return HttpResponse(f'Доступный максимум 3статьи за сутки.Вы разместили {len(post_list)}')

    def post(self, request, *args, **kwargs):
        print(request.user)
        p = Post(title=request.POST['title'],
                 post_content=request.POST['post_content'],
                 post_type=request.POST['post_type'],
                 author_name=Author.objects.get(id=request.POST['author_name']),
                 )
        p.save()
        subscribers_list = []
        email_list = set()
        selected_categories = request.POST.getlist('post_category')
        for i in selected_categories:
            p.post_category.add(i)
            subscribers_list.append(User.objects.filter(cats=i))

        for user_obj in subscribers_list:
            for i in user_obj:
                email_list.add(i.email)
        email_list = list(email_list)

        announce.delay(p.pk, email_list)
        return redirect('allnews')

    # Реализация рассылки без использования сигналов.
    # def post(self, request, *args, **kwargs):
    #     p = Post(title=request.POST['title'],
    #              post_content=request.POST['post_content'],
    #              post_type=request.POST['post_type'],
    #              author_name=Author.objects.get(id=request.POST['author_name']),
    #              )
    #     p.save()
    #     subscribers_list = []
    #     email_list = set()
    #     selected_categories = request.POST.getlist('post_category')
    #     for i in selected_categories:
    #         p.post_category.add(i)
    #         subscribers_list.append(User.objects.filter(cats=i))
    #
    #     for user_obj in subscribers_list:
    #         for i in user_obj:
    #             email_list.add(i.email)
    #     email_list = list(email_list)
    #
    #     html_content = render_to_string('mailing.html', {
    #         'news_id': p.id,
    #         'news_preview': p.preview()
    #     })
    #     msg = EmailMultiAlternatives(subject=f'{p.title}',
    #                                  body='',
    #                                  from_email=settings.DEFAULT_FROM_EMAIL,
    #                                  to=email_list)
    #     msg.attach_alternative(html_content, "text/html")
    #     msg.send()
    #
    #     return redirect('allnews')


class UpdateNews(PermissionRequiredMixin, UpdateView):
    form_class = CreateForm
    model = Post
    template_name = 'updatenews.html'
    permission_required = ('news.change_post',)
    raise_exception = True


class ErasingNews(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'deletenews.html'
    success_url = reverse_lazy('allnews')
    permission_required = ('news.delete_post',)
    raise_exception = True


class CategoryView(ListView):
    model = Post
    template_name = 'categories.html'
    context_object_name = 'categorylist'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_subscriber'] = self.request.user in self.category.subscribers.all()
        context['cat'] = self.category
        return context


@login_required
def subscribe_user(request, pk):
    subscriber = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(subscriber)

    message = f'Вы успешно подписались на новости {category} категории'
    context = {'message': message, 'category': category}
    return render(request, 'subscribe.html', context)

@login_required
def unsubscribe_user(request, pk):
    subscriber = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(subscriber)

    message = f'Вы отписались от рассылки новостей {category} категории'
    context = {'message': message, 'category': category}
    return render(request, 'unsubscribe.html', context)