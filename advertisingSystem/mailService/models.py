from django.db import models

# Create your models here.


class Mail(models.Model):
    advertise = models.ForeignKey('Submission.Advertise', on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)