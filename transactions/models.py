from django.db import models

# Create your models here.
from accounts.models import User


class Calorie(models.Model):


    title = models.CharField(max_length=200,null=True)

    serving_size = models.CharField(max_length=200,null=True)

    calorie = models.FloatField(null=True)

    MEAL_CHOICES = [
        ("break_fast", "break_fast"),
        ("lunch", "lunch"),
        ("snacks","snacks"),
        ("dinner","dinner"),
    ]

    meal_type = models.CharField(max_length=20,choices=MEAL_CHOICES,default="break_fast")

    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    created_at = models.DateField(auto_now_add=True)