# Generated by Django 5.0.6 on 2024-05-27 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watch_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cat',
            field=models.IntegerField(choices=[(1, 'Men Watch'), (2, 'Women Watch'), (3, 'children'), (4, 'Stylish'), (5, 'Sports'), (6, 'Wall Watch')], verbose_name='Category'),
        ),
    ]