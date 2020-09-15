from django import forms
from Biblioteka.models import Ksiazka
from django.contrib.auth.models import User


class NowaKsiazka(forms.ModelForm):
    tytul = forms.CharField(label="Tytuł książki:", max_length=100)
    autor = forms.CharField(label="Autor książki:", max_length=100)
    typ_okladki = forms.ChoiceField(label="Typ okładki",choices=Ksiazka.typy_okladki)
    wydawnictwo = forms.CharField(label="Wydawnictwo:", max_length=100)
    data_premiery = forms.DateField(label="Data premiery:")
    liczba_stron = forms.IntegerField(label="Liczba stron:")
    zdjecie = forms.FileField(label="Wybierz zdjęcie")

    class Meta:
        model = Ksiazka
        fields = ['tytul', 'autor', 'typ_okladki', 'wydawnictwo', 'data_premiery', 'liczba_stron']

class LoginForm(forms.ModelForm):
    nazwa_uzytkownika = forms.CharField(label="Nazwa użytkownika", max_length=150)
    haslo = forms.CharField(label="Hasło", max_length=50, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['nazwa_uzytkownika', 'haslo']