from django.urls import path
from .views import NewsList, DefiniteNews

urlpatterns = [path('', NewsList.as_view()),
               path('<int:pk>', DefiniteNews.as_view()),
               ]