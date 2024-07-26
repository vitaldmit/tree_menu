from django import template
from django.urls import resolve
from ..models import MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')
    
    def build_menu(items, parent=None):
        menu = []
        for item in items:
            if item.parent == parent:
                children = build_menu(items, item)
                is_active = current_url.startswith(item.get_url())
                menu.append({
                    'item': item,
                    'children': children,
                    'is_active': is_active,
                })
        return menu

    menu = build_menu(menu_items)
    return {'menu': menu, 'current_url': current_url}

@register.filter
def is_expanded(item, current_url):
    if item['is_active']:
        return True
    if any(child['is_active'] for child in item['children']):
        return True
    return False
