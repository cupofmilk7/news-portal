from django import template
from django.utils.safestring import mark_safe
from home.models import Author

register = template.Library()


@register.simple_tag(takes_context=True)
def author_tag(context):
    author = Author.objects.first()
    if not author:
        return ""
    return mark_safe(f"""
        <footer class="author">
            <p>{author.name}</p>
            <p>{author.email}</p>
        </footer>
    """)