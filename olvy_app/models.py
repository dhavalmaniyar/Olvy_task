import datetime
from datetime import date
from email.policy import default
from django.db import models
# Create your models here.


class user(models.Model):
    user_id = models.CharField(primary_key=True, max_length=70, editable=False)
    user_name = models.CharField(max_length=70, null=False)

    def __str__(self):
        return self.user_name


class product(models.Model):
    product_id = models.CharField(
        primary_key=True, max_length=70, editable=False)
    x = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
    }
    ratings = models.JSONField(default=x)


class review(models.Model):
    reviewerID = models.ForeignKey(user, on_delete=models.CASCADE)
    asin = models.ForeignKey(product, on_delete=models.CASCADE)
    helpful = models.IntegerField()
    reviewText = models.TextField()
    overall = models.FloatField(null=False)
    summary = models.CharField(max_length=70)
    unixReviewTime = models.IntegerField(null=False, editable=False)
