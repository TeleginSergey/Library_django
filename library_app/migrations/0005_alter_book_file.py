# Generated by Django 4.1.7 on 2024-05-10 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0004_book_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='static/'),
        ),
    ]
