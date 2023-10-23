from django.db import models

class Population(models.Model):
    name = models.CharField(max_length=10)
    male = models.PositiveIntegerField(default=0)
    female = models.PositiveIntegerField(default=0)
    def total(self):
        return int(self.male + self.female)
    def __str__(self):
        return self.name
