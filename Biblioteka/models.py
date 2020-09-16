from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


class Ksiazka(models.Model):
    tytul = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    typy_okladki = (
        ('miekka', 'Okladka miekka'),
        ('twarda', 'Okladka twarda')
    )
    typ_okladki = models.CharField(choices=typy_okladki, max_length=20, default=None)
    wydawnictwo = models.CharField(max_length=100)
    data_premiery = models.DateField(default=None)
    data_publikacji = models.DateTimeField(default=None)
    liczba_stron = models.IntegerField(default=None)
    uzytkownik = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    zdjecie = models.FileField(null=True, default=None,
                               validators=[FileExtensionValidator(allowed_extensions=['jpg','png','jpeg'])])
    czy_aktywna = models.BooleanField(default=True)