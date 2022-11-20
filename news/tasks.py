from datetime import datetime, timedelta

from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category
from project import settings
from project.settings import SITE_URL

from project.celery import app


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(n):
    for i in range(n):
        time.sleep(1)
        print(i + 1)


@shared_task
def weekly_announcement():
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    posts = Post.objects.filter(post_creation_date__gte=week_ago)
    categories = set(posts.values_list('post_category__category', flat=True))
    subscribers = set(Category.objects.filter(category__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string('weekly_posts.html', {
        'link': f'{SITE_URL}',
        'posts': posts,
        'date': week_ago,
    })
    msg = EmailMultiAlternatives(subject='Статьи за неделю',
                                 body='',
                                 from_email=settings.DEFAULT_FROM_EMAIL,
                                 to=list(subscribers), )
    msg.attach_alternative(html_content, 'text/html')

    msg.send()


@app.task
def announce(post_id, emails):
    p = Post.objects.get(id=post_id)
    html_content = render_to_string('mailing.html', {
        'news_preview': p.preview(),
        'link': f'{SITE_URL}/news/{p.pk}'
    })
    msg = EmailMultiAlternatives(subject=f'{p.title}',
                                 body='',
                                 from_email=settings.DEFAULT_FROM_EMAIL,
                                 to=emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()