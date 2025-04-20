from django.db import models
from django.urls import reverse

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.
class Bird(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.TextField()
    age = models.IntegerField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'bird_id': self.id})


class Feeding(models.Model):
    date = models.DateField('Feeding Date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0],
    )
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"