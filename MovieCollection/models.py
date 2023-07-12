from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='covers/')
    category = models.ManyToManyField('Category')
    actors = models.ManyToManyField('Actor')

    def __str__(self):
        return self.title

class Actor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name