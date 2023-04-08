import logging
import datetime

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from portal_app.models import Category
import os
from dotenv import load_dotenv


MY_EMAIL = os.getenv('MY_EMAIL')

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def weekly_notifier():
    category_count = Category.objects.all().count()
    seven_days_ago = timezone.now() - datetime.timedelta(days=7)

    for i in range(1, category_count + 1):
        category = Category.objects.get(id=i)
        subscribers = category.subscribers.all()
        for subscriber in subscribers:
            username = subscriber.user.username
            posts = category.posts.filter(post_created__gte=seven_days_ago)

            html_content = render_to_string(
                'weekly_notifier.html',
                {
                    'category_name': category.name,
                    'posts': posts,
                    'username': username,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'Дайджест постов в категории {category.name} за прошедшую неделю',
                body='К сожалению, возникли проблемы с рендерингом HTML',
                # Body текст будет выслан, если не сработает HTML версия
                from_email=MY_EMAIL + '@yandex.com',
                to=[subscriber.user.email],  # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()  # отсылаем


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            weekly_notifier,
            trigger=CronTrigger(second="*/30"),
            id="weekly_notifier",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_notifier'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
