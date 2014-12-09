from django.db import models

class Redirection(models.Model):
    real_url = models.URLField(unique=True)
    small_url = models.CharField(max_length=42, unique=True)
    pseudo = models.CharField(max_length=42)
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date de parution")
    number_access = models.IntegerField(default=0)

    def __str__(self):
           return self.real_url + "$" + self.small_url
