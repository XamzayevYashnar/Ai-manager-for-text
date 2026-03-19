from django import template
from editor.models import PagesAi

register = template.Library()

@register.simple_tag(name='get_pages')
def get_page_ai(user_id):
    if user_id is None:
        pages = PagesAi.objects.all()
    else:
        pages = PagesAi.objects.filter(user_id=user_id)

@register.inclusion_tag("ai/list_pages.html")
def show_pages(user_id, slug):
    if user_id is None:
        pages = PagesAi.objects.all()
    else:
        pages = PagesAi.objects.filter(user_id=user_id)

    return {"pages": pages, "slug": slug}