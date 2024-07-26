from django import template
from django.urls import resolve
from ..models import MenuItem

register = template.Library()

@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['request'].path
    menu_items = MenuItem.objects.filter(menu_name=menu_name, parent=None)
    
    def process_menu_items(items):
        for item in items:
            item.is_expanded = should_expand(item, current_url)
            if item.children.exists():
                process_menu_items(item.children.all())
    
    process_menu_items(menu_items)
    
    return {
        'menu_items': menu_items,
        'current_url': current_url,
    }


@register.filter
def is_expanded(item, current_url):
    if item['is_active']:
        return True
    if any(child['is_active'] for child in item['children']):
        return True
    return False

def should_expand(item, current_url):
    if item.url == current_url:
        return True
    if current_url.startswith(item.url) and item.url != '/':
        return True
    return False