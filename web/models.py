from django.db import models


class JobPost(models.Model):
  job_id = models.CharField(max_length=20)
  text = models.CharField(max_length=255)
  link = models.CharField(max_length=200)
  location = models.CharField(max_length=100)
  company = models.CharField(max_length=100)
  description = models.TextField()
  posted = models.CharField(max_length=20)
