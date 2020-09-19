from django.utils import timezone

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from PIL import Image

from .models import Ksiazka
from Biblioteka.forms import NowaKsiazka, LoginForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from .serializers import KsiazkaSerializer
from rest_framework.response import Response
from rest_framework import status

def wypisz_wszystkie_ksiazki(request):
    wszystkie_ksiazki = Ksiazka.objects.all()
    context = {'wszystkie_ksiazki': wszystkie_ksiazki}
    return render(request, 'Biblioteka/index.html', context)

def dodaj_ksiazke(request):
    if request.method == "POST":
        form = NowaKsiazka(request.POST, request.FILES)
        if form.is_valid():
            ksiazka = form.save(commit = False)
            ksiazka.uzytkownik = request.user
            ksiazka.data_publikacji = timezone.now()
            ksiazka.data_premiery = request.POST['data_premiery']
            ksiazka.tytul = request.POST['tytul']
            ksiazka.autor = request.POST['autor']
            ksiazka.typ_okladki = request.POST['typ_okladki']
            ksiazka.wydawnictwo = request.POST['wydawnictwo']
            ksiazka.liczba_stron = request.POST['liczba_stron']
            ksiazka.zdjecie = request.FILES['zdjecie']
            ksiazka.save()
            return redirect('/', pk=ksiazka.pk)
    else:
        form = NowaKsiazka()
    return render(request, 'Biblioteka/nowaksiazka.html', {'form': form})
def logowanie(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid:
            user = authenticate(username = request.POST['nazwa_uzytkownika'], password = request.POST['haslo'])
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                return HttpResponse("<p> Niepoprawne dane logowania </p>")
    else:
        form = LoginForm()
    return render(request, 'Biblioteka/login.html', {'form': form})
def panel_uzytkownika(request):
    return render(request, 'Biblioteka/panel.html')
def wyswietl_ksiazki_uzytkownika(request):
    ksiazki_uzytkownika = Ksiazka.objects.all().filter(uzytkownik=request.user)
    context = {'ksiazki_uzytkownika': ksiazki_uzytkownika}
    return render(request, 'Biblioteka/ksiazki.html', context)
def wyloguj(request):
    if request.user is not None:
        logout(request)
    return redirect('index')
def usun_ksiazke(request, pk):
    object = get_object_or_404(Ksiazka, pk=pk)
    context = {'pk': pk}
    if object.czy_aktywna == True:
        object.czy_aktywna = False
        object.save()
        return render(request, 'Biblioteka/usunksiazke.html', context)
    return HttpResponse('Książka jest już usunięta')
def opublikuj_ksiazke(request,pk):
    object = get_object_or_404(Ksiazka, pk=pk)
    context = {'pk': pk}
    if object.czy_aktywna == False:
        object.czy_aktywna = True
        object.data_publikacji = timezone.now()
        object.save()
        return render(request, 'Biblioteka/opublikujksiazke.html', context)
    return HttpResponse('Książka jest już opublikowana')
def edytuj_ksiazke(request, pk):
    object = get_object_or_404(Ksiazka, pk=pk)
    if request.method == "POST":
        form = NowaKsiazka(request.POST, request.FILES, instance=object)
        if form.is_valid():
            object = form.save(commit=False)
            object.uzytkownik = request.user
            object.data_publikacji = timezone.now()
            object.data_premiery = request.POST['data_premiery']
            object.tytul = request.POST['tytul']
            object.autor = request.POST['autor']
            object.typ_okladki = request.POST['typ_okladki']
            object.wydawnictwo = request.POST['wydawnictwo']
            object.liczba_stron = request.POST['liczba_stron']
            object.zdjecie = request.FILES['zdjecie']
            object.save()
            return redirect('index')
    else:
        form = NowaKsiazka(instance=object)
    return render(request, 'Biblioteka/edytujksiazke.html', {'form': form})
class KsiazkaView(viewsets.ModelViewSet):
    queryset = Ksiazka.objects.all()
    serializer_class = KsiazkaSerializer

    def create(self, request, *args, **kwargs):
        serializer = KsiazkaSerializer()
        if serializer.is_valid and request.method == "POST":
            ksiazka = Ksiazka.objects.create(tytul = request.data['tytul'], autor = request.data['autor'],
                                            typ_okladki = request.data['typ_okladki'],
                                            wydawnictwo = request.data['wydawnictwo'], data_premiery = request.data['data_premiery'],
                                            data_publikacji = timezone.now(), liczba_stron = request.data['liczba_stron'],
                                            uzytkownik = self.request.user, zdjecie = request.data['zdjecie'], czy_aktywna = True)
            ksiazka.save()
            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        ksiazka = self.get_object()
        if ksiazka.czy_aktywna is True and request.method == "DELETE":
            ksiazka.czy_aktywna = False
            ksiazka.save()
            return Response("Usunięto książkę")
        return Response("Książka nie jest aktywna")

    def update(self, request, *args, **kwargs):
        ksiazka = self.get_object()
        serializer = KsiazkaSerializer(ksiazka, data = request.data)
        if serializer.is_valid() and request.method == "PUT":
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)
