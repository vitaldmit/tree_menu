from django.shortcuts import render
from .models import MenuItem


def home(request):
    menu_items = MenuItem.objects.filter(parent=None)
    return render(request, 'home.html', {'menu_items': menu_items})


def menu_page(request, menu_path=''):
    current_url = '/' + menu_path
    menu_items = MenuItem.objects.filter(parent=None)
    return render(request, 'menu_page.html', {
        'menu_items': menu_items,
        'current_url': current_url
    })
