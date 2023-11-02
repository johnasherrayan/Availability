# Generated by Django 4.2.6 on 2023-11-01 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('availability_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='campaign_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to='availability_tracker.campaign'),
        ),
        migrations.CreateModel(
            name='LidarMeasurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('height', models.FloatField()),
                ('wind_speed', models.FloatField()),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lidar_measurements', to='availability_tracker.campaign')),
            ],
        ),
    ]
