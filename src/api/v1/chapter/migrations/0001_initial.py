# Generated by Django 4.2.11 on 2024-03-22 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('composition', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Номер главы')),
                ('created', models.DateField(auto_now_add=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')),
                ('is_published', models.BooleanField(default=False)),
                ('pub_date', models.DateTimeField(blank=True, null=True)),
                ('composition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='composition.composition')),
            ],
            options={
                'ordering': ['number'],
                'unique_together': {('number', 'composition')},
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Номер страницы')),
                ('image_page', models.ImageField(upload_to='images/chapter_page/', verbose_name='Изображение страницы')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chapter.chapter')),
            ],
            options={
                'unique_together': {('number', 'chapter')},
            },
        ),
    ]
