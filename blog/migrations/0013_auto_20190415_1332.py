# Generated by Django 2.2 on 2019-04-15 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_remove_book_authors'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='Publisher',
        ),
    ]
