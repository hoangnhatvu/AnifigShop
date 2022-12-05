from .models import Category, Product

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)