# Generated by Django 4.2.11 on 2024-03-24 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=500, verbose_name='Текст комментария'),
        ),
    ]
