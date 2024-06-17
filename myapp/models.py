from django.db import models
from django.contrib.auth.models import User

class Food(models.Model):

    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)
    carbs = models.FloatField()
    protein = models.FloatField()
    fats = models.FloatField()
    calories = models.IntegerField()


class Consume(models.Model):

    def __str__(self):
        return f"{self.user} => {self.food_consumed}"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_consumed = models.ForeignKey(Food, on_delete=models.CASCADE)