# Generated by Django 3.1.5 on 2021-03-29 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_reviews', '0007_auto_20210329_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='stars',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
