# Generated by Django 2.0.6 on 2018-08-10 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0020_auto_20180807_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articledetail',
            name='article',
            field=models.OneToOneField(on_delete=None, to='repository.Article', verbose_name='所属文章'),
        ),
        migrations.AlterField(
            model_name='updown',
            name='up',
            field=models.NullBooleanField(verbose_name='是否赞'),
        ),
    ]
