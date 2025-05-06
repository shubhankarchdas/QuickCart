from category.service import get_all_categories


def menu_links(request):
    links = get_all_categories()
    return dict(links=links)