# Generated by Django 4.1.6 on 2023-04-04 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_app', '0005_alter_subscriber_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subscriber',
        ),
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscribed_categories', through='portal_app.CategorySubscriber', to='portal_app.subscriber'),
        ),
    ]