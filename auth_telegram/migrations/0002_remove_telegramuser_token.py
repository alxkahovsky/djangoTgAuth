# Generated by Django 5.1.3 on 2024-12-02 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_telegram', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramuser',
            name='token',
        ),
    ]
