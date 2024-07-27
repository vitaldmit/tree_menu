from django import template
from ..models import MenuItem

register = template.Library()


@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')  # E501

    def build_menu_tree(items):
        tree = []
        item_dict = {item.id: item for item in items}
        for item in items:
            item.subchildren = []
            if item.parent_id:
                parent = item_dict[item.parent_id]
                parent.subchildren.append(item)
            else:
                tree.append(item)
        return tree

    def set_expanded(item, current_url, level=0):
        item.is_expanded = item.url == current_url or current_url.startswith(item.url)
        if item.is_expanded:
            item.active_level = level
        for child in item.subchildren:
            child_expanded = set_expanded(child, current_url, level + 1)
            item.is_expanded = item.is_expanded or child_expanded
        return item.is_expanded

    menu_tree = build_menu_tree(menu_items)
    for item in menu_tree:
        set_expanded(item, current_url)

    return {
        'menu_items': menu_tree,
        'current_url': current_url,
    }


def is_expanded(item, current_url):
    return item.url == current_url or current_url.startswith(item.url)


def should_expand(item, current_url):
    if item.url == current_url:
        return True
    if current_url.startswith(item.url) and item.url != '/':
        return True
    return any(should_expand(child, current_url) for child in item.children.all())
