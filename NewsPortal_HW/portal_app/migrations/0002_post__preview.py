# Generated by Django 4.1.5 on 2023-02-06 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='_preview',
            field=models.CharField(db_column='preview', max_length=200, null=True),
        ),
    ]
