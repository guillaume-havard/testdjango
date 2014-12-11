from django.db import models
import random
import string

class Redirection(models.Model):
    real_url = models.URLField(unique=True)
    small_url = models.CharField(max_length=42, unique=True)
    pseudo = models.CharField(max_length=42)
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date de parution")
    number_access = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.generer(6)

        super(Redirection, self).save(*args, **kwargs)

    def generer(self, nb_caracteres):
        caracteres = string.ascii_letters + string.digits
        aleatoire = [random.choice(caracteres) for _ in range(nb_caracteres)]

        self.small_url = ''.join(aleatoire)

    def __str__(self):
           return self.real_url + "$" + self.small_url
