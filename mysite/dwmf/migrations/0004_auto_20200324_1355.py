# Generated by Django 3.0.3 on 2020-03-24 20:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwmf', '0003_auto_20200324_1246'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created_date']},
        ),
        migrations.AlterField(
            model_name='review',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 24, 13, 55, 40, 477028)),
        ),
    ]