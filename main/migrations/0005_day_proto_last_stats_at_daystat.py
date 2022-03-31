# Generated by Django 4.0.2 on 2022-03-23 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_order_scraped_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('day', models.DateField(db_index=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='proto',
            name='last_stats_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.CreateModel(
            name='DayStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('qty_on_sale', models.IntegerField(null=True)),
                ('lowest_price', models.FloatField(null=True)),
                ('runner_price', models.FloatField(null=True)),
                ('act_prc7', models.FloatField(null=True)),
                ('act_prc14', models.FloatField(null=True)),
                ('act_prc30', models.FloatField(null=True)),
                ('act_prc60', models.FloatField(null=True)),
                ('act_vol7', models.IntegerField(null=True)),
                ('act_vol14', models.IntegerField(null=True)),
                ('act_vol30', models.IntegerField(null=True)),
                ('act_vol60', models.IntegerField(null=True)),
                ('last_price', models.FloatField(null=True)),
                ('fil_prc7', models.FloatField(null=True)),
                ('fil_prc14', models.FloatField(null=True)),
                ('fil_prc30', models.FloatField(null=True)),
                ('fil_prc60', models.FloatField(null=True)),
                ('fil_vol7', models.IntegerField(null=True)),
                ('fil_vol14', models.IntegerField(null=True)),
                ('fil_vol30', models.IntegerField(null=True)),
                ('fil_vol60', models.IntegerField(null=True)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daystats', to='main.day')),
                ('proto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daystats', to='main.proto')),
            ],
            options={
                'unique_together': {('proto', 'day')},
            },
        ),
    ]
