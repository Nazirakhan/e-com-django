# it takes a request as an argument and it will return the dictionary of data as a context
from . models import Category


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)

# def scroll_position(request):
#     scroll_position = request.COOKIES.get('scroll_position', 0)
#     return {'scroll_position': scroll_position}