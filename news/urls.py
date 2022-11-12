from django.urls import path
from .views import *

urlpatterns = [path('', NewsList.as_view(), name='allnews'),
               path('<int:pk>', DefiniteNews.as_view(), name='definitenews'),
               path('search/', SearchNews.as_view(), name='news-search'),
               path('create/', CreateNews.as_view(), name='news-creation'),
               path('<int:pk>/update/', UpdateNews.as_view(), name='news-update'),
               path('<int:pk>/delete/', ErasingNews.as_view(), name='news-delete'),
               path('category/<int:pk>', CategoryView.as_view(), name='category'),
               path('category/<int:pk>/subscribe', subscribe_user, name='subscribing'),
               path('category/<int:pk>/unsubscribe', unsubscribe_user, name='unsubscribing'),
               ]