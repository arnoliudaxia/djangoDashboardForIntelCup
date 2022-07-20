# Generated by Django 3.2.13 on 2022-07-20 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labdbAPI', '0006_meter_config_belonglab'),
    ]

    operations = [
        migrations.CreateModel(
            name='ai_process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField()),
                ('takeinVideo', models.TextField()),
                ('belong2Meter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labdbAPI.meter_config')),
            ],
        ),
    ]
