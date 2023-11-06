# Generated by Django 4.2.6 on 2023-11-06 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcation',
            name='order_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Order ID'),
        ),
        migrations.AddField(
            model_name='transcation',
            name='payment_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Payment ID'),
        ),
        migrations.AddField(
            model_name='transcation',
            name='signature',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Signature'),
        ),
    ]
