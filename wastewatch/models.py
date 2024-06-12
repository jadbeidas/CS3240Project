from django.db import models
from django.conf import settings
from django.utils import timezone
from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.auth.models import User



class Report(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.TextField(max_length=100)
    description = models.TextField(max_length=500)
    text_file = models.FileField()
    image_file = models.ImageField()
    date = models.DateTimeField(help_text="Select the time of the report")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    REPORT_STATUS = (
        (0, 'New'),
        (1, 'In Progress'),
        (2, 'Resolved'),
    )
    status = models.PositiveSmallIntegerField(choices=REPORT_STATUS, default=0)
    resolve_explanation = models.TextField(null=True, max_length=500)


class ReportStorage(S3Boto3Storage):
    location = 'reports'
    default_acl = 'public-read'
    file_overwrite = False
