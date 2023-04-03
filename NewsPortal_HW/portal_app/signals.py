from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Subscriber, CategorySubscriber, PostCategory
from django.core.mail import send_mail
from dotenv import load_dotenv
import os

load_dotenv()
MY_EMAIL = os.getenv('MY_EMAIL')

@receiver(post_save, sender=PostCategory)
def new_post_email_to_subscribers(sender, instance, created, **kwargs):
    print('sender=PostCategory')
    if created:  # Only execute the following code when a new PostCategory instance is created
        post = instance.post
        title = post.title
        author = post.author.user.username
        category = instance.category
        print(f'Author: {author} and Category: {category.name}')

        # Get the subscribers for the category of the post
        subscribers = CategorySubscriber.objects.filter(category=category)

        # Extract the email addresses from the subscribers
        recipient_list = [subscriber.user.email for subscriber in subscribers]
        print(recipient_list)

        # Send an email notification to the subscribers
        subject = f'Новая статься в категории: {category.name}'
        message = f'Новая статья {title} от {author} в категории: {category.name}'
        from_email = MY_EMAIL + '@yandex.com'
        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

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


# @receiver(post_save, sender=Post)
# def new_post_email_to_subscribers(sender, instance, **kwargs):
#     title = instance.title
#     author = instance.author.user.username
#     category = instance.category.name
#     # Get the subscribers for the category of the post
#     subscribers = CategorySubscriber.objects.filter(category=instance.category)
#
#     # Extract the email addresses from the subscribers
#     recipient_list = [subscriber.user.email for subscriber in subscribers]
#
#
#     # Send an email notifica to the subscribers
#     subject = f'Новая статься в категории: {category}'
#     message = f'Новая статья {title} от {author} в категории: {category}'
#     from_email = MY_EMAIL + '@yandex.com'
#     send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

