# Generated by Django 2.2.7 on 2019-11-25 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20191125_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='venue_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Venue'),
        ),
    ]