from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime

from .models import Subscriber, CategorySubscriber, Post, Category
from django.core.mail import send_mail, EmailMultiAlternatives
from dotenv import load_dotenv
import os

load_dotenv()
MY_EMAIL = os.getenv('MY_EMAIL')

# Сигнал отключен, т.к. заменен на Celery
# @receiver(m2m_changed, sender=Post.categories.through)
# def new_post_email_to_subscribers(sender, instance, action, pk_set, **kwargs):
#     if action == 'post_add':
#         title = instance.title
#         author_name = instance.author.user.username
#
#         for i in range(len(pk_set)):        # going through each of categories
#             category_id = list(pk_set)[i]
#             category = Category.objects.get(pk=category_id)
#
#             # Get the subscribers for the category of the post
#             subscribers = category.subscribers.all() #subscribers is a related name, defined in the Model
#             # Extract the email addresses from the subscribers
#             recipient_list = [subscriber.user.email for subscriber in subscribers]
#
#             html_content = render_to_string(
#                 'new_post_email_to_subscribers.html',
#                 {
#                     'post': instance,
#                     'category': category
#                 }
#             )
#
#             msg = EmailMultiAlternatives(
#                 subject=f'Новая статья в категории "{category.name}"',
#                 body='К сожалению, возникли проблемы с рендерингом HTML',
#                 # Body текст будет выслан, если не сработает HTML версия
#                 from_email=MY_EMAIL + '@yandex.com',
#                 to=recipient_list,  # это то же, что и recipients_list
#             )
#             msg.attach_alternative(html_content, "text/html")  # добавляем html
#
#             msg.send()  # отсылаем


# Этот сигнал нужен для создания объекта Подписчик (если токого нет), когда пользователь логинится
@receiver(user_logged_in)
def create_subscriber(sender, user, request, **kwargs):
    subscriber, created = Subscriber.objects.get_or_create(user=user)


@receiver(post_save, sender=CategorySubscriber)
def subscription_confirmation_email(sender, instance, **kwargs):
    category = instance.category
    subscriber = instance.subscriber
    print(f'category: {category.name} and subscriber email: {subscriber.user.email}')

    # Send an email confirmation to the subscriber
    subject = f'Подтверждение подписки на категорию: {category.name}'
    message = 'Ура, подписка успешна!'
    from_email = MY_EMAIL + '@yandex.com'
    recipient_list = [subscriber.user.email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

@receiver(post_save, sender=User)
def welcome_email(sender, instance, created, **kwargs):
    print("before if_created")
    if created:
        print("during if_created")
        html_content = render_to_string(
            'account/welcome_new_user.html',
            {
                'user': instance,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Регистрация успешна!',
            body=f'''{instance.username}, добро пожаловать в Новостной Портал!
                 Вы зарегистрировались при помощи почтового ящика: {instance.email}''',
            #Body текст будет выслан, если не сработает HTML версия
            from_email=MY_EMAIL + '@yandex.com',
            to=[instance.email],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем

        return redirect(settings.LOGIN_URL)
    print("after if_created")


@receiver(pre_save, sender=Post)
def limit_check(sender, instance, **kwargs):
    if not instance.pk: #нас интересуют только новые статьи, поэтому убеждаемся что статьи НЕТ в базе
        today = datetime.now().date()
        author_posts_today = len(Post.objects.filter(post_created__date=today, author=instance.author))
        if author_posts_today >= 3:
            raise ValidationError("Превышено ограничение в 3 поста/день")
