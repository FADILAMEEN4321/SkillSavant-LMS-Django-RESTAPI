# Generated by Django 4.2.6 on 2023-11-21 04:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chatmessage_timestamp'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ChatMessage',
        ),
    ]