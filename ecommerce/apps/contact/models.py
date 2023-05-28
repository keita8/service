import datetime
from django.utils import timezone
from django.db import models



class Contact(models.Model):
    name = models.CharField(max_length = 150, verbose_name="nom")
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length = 150, verbose_name='objet')
    message = models.TextField()
    timestamp = models.DateTimeField("date", default= timezone.now)


    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.name

