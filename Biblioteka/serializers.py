from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from .models import Ksiazka
from .validators import validate_file_extension
from PIL import Image

class KsiazkaSerializer(serializers.ModelSerializer):
    tytul = serializers.CharField(label="Tytuł książki:", max_length=100)
    autor = serializers.CharField(label="Autor książki:", max_length=100)
    typ_okladki = serializers.ChoiceField(label="Typ okładki", choices=Ksiazka.typy_okladki)
    wydawnictwo = serializers.CharField(label="Wydawnictwo:", max_length=100)
    data_premiery = serializers.DateField(label="Data premiery:")
    liczba_stron = serializers.IntegerField(label="Liczba stron:")
    zdjecie = serializers.ImageField(label="Wybierz zdjęcie", validators=[validate_file_extension],
                                    )

    class Meta:
        model = Ksiazka
        fields = ['tytul', 'autor', 'typ_okladki', 'wydawnictwo', 'data_premiery', 'liczba_stron','zdjecie']

