# Generated by Django 4.0.2 on 2022-03-20 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proto',
            name='effect',
            field=models.CharField(max_length=500, null=True),
        ),
    ]