"""projekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from Biblioteka import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.wypisz_wszystkie_ksiazki, name = 'index'),
    path('panel/nowaksiazka/', views.dodaj_ksiazke, name = 'dodajksiazke'),
    path('login/', views.logowanie, name='login'),
    path('panel/', views.panel_uzytkownika, name='panel'),
    path('panel/ksiazki/', views.wyswietl_ksiazki_uzytkownika, name='ksiazki'),
    path('panel/logout/', views.wyloguj, name="logout"),
    path('panel/ksiazki/<pk>/usunksiazke/', views.usun_ksiazke, name='usunksiazke'),
    path('panel/ksiazki/<pk>/opublikujksiazke/', views.opublikuj_ksiazke, name='opublikujksiazke'),
    path('panel/ksiazki/<pk>/edytujksiazke/', views.edytuj_ksiazke, name='edytujksiazke')
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
