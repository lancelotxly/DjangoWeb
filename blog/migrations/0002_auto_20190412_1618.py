# Generated by Django 2.2 on 2019-04-12 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testtable',
            name='email',
            field=models.EmailField(default=None, max_length=254),
        ),
        migrations.AddField(
            model_name='testtable',
            name='text',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='testtable',
            name='age',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='testtable',
            name='gender',
            field=models.BooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='testtable',
            name='name',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='testtable',
            name='salary',
            field=models.FloatField(default=None),
        ),
    ]
