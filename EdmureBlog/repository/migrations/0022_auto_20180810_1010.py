# Generated by Django 2.0.6 on 2018-08-10 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0021_auto_20180810_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updown',
            name='up',
            field=models.BooleanField(default=False, verbose_name='是否赞'),
        ),
    ]
