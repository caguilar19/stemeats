# Generated by Django 2.0.7 on 2018-08-08 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodblog', '0002_auto_20180808_0131'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='restaurant',
            field=models.ManyToManyField(related_name='posts', to='foodblog.Restaurant'),
        ),
    ]
