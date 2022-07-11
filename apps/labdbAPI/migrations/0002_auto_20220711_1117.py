# Generated by Django 3.2.13 on 2022-07-11 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labdbAPI', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meter_config',
            name='id',
        ),
        migrations.RemoveField(
            model_name='meter_config',
            name='pub_date',
        ),
        migrations.RemoveField(
            model_name='meter_config',
            name='question_text',
        ),
        migrations.AddField(
            model_name='meter_config',
            name='meterGUID',
            field=models.CharField(default=2, max_length=36, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meter_config',
            name='meterName',
            field=models.TextField(default='表'),
        ),
    ]
