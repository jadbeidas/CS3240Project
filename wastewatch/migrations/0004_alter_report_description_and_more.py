# Generated by Django 4.2.11 on 2024-04-15 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wastewatch', '0003_report_latitude_report_longitude_alter_report_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='description',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='report',
            name='resolve_explanation',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='title',
            field=models.TextField(max_length=100),
        ),
    ]