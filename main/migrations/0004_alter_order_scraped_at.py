# Generated by Django 4.0.2 on 2022-03-21 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_order_scraped_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='scraped_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
