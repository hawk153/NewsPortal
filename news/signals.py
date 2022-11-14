from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import Q
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, PostCategory, Author, Category
from project.settings import SITE_URL


def announce(preview, pk, title, subscriber):
    for i in subscriber:
        html_content = render_to_string('mailing.html', {'news_preview': preview,
                                                         'link': f'{SITE_URL}/news/{pk}',
                                                         'name': i
                                                         })
        msg = EmailMultiAlternatives(subject=f'{title}',
                                     body='',
                                     from_email=settings.DEFAULT_FROM_EMAIL,
                                     to=[i])
        msg.attach_alternative(html_content, 'text/html')

        msg.send()


@receiver(m2m_changed, sender=PostCategory)
def new_post_announcing(sender, instance, **kwargs, ):
    if kwargs['action'] == 'post_add':
        c = instance.post_category.all()
        subscribers = list()
        for category in c:
            subscribers += category.subscribers.all()

        subscribers = [i.email for i in subscribers]
        announce(instance.preview(), instance.pk, instance.title, subscribers)


# @receiver(post_save, sender=Post)
# def post_restriction(sender, instance, **kwargs):
#     time_now = datetime.now()
#     time_day_ago = time_now - timedelta(hours=24)
#     post_list = Post.objects.filter(Q(post_creation_date__gte=time_day_ago) &
#                                     Q(post_creation_date__lte=time_now) & Q(author_name=instance.author_name))
#
#
#
#     if len(post_list) > 3:
#         instance.delete()