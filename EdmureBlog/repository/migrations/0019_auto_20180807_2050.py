# Generated by Django 2.0.6 on 2018-08-07 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0018_auto_20180807_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=None, to='repository.Category', verbose_name='文章类型'),
        ),
        migrations.AlterField(
            model_name='article2tag',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=None, to='repository.Tag', verbose_name='标签'),
        ),
    ]