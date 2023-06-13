from django.db import models

class Title(models.Model):
    pass

class Review(models.Model):
    author = models.ForeignKey(
        Title,
        verbose_name=("Отзыв"),
        on_delete=models.CASCADE,
        
    )