# Generated by Django 4.2.11 on 2024-03-31 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email_not',
            field=models.BooleanField(default=False, verbose_name='Уведомления на почту'),
        ),
    ]
