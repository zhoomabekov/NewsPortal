# Generated by Django 4.1.6 on 2023-03-17 23:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal_app', '0003_alter_post_title_alter_post_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CategorySubscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal_app.category')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal_app.subscriber')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='subscriber',
            field=models.ManyToManyField(related_name='subscribers', through='portal_app.CategorySubscriber', to='portal_app.subscriber'),
        ),
    ]