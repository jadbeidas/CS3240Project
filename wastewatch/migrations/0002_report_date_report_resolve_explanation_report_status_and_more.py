# Generated by Django 5.0.1 on 2024-03-29 19:09

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wastewatch', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='report',
            name='resolve_explanation',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'New'), (1, 'In Progress'), (2, 'Resolved')], default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
