# Generated by Django 4.2.6 on 2023-11-16 03:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_remove_chatmessage_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]