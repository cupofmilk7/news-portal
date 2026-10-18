from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from modelcluster.fields import ParentalManyToManyField

from wagtail.snippets.models import register_snippet


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('email'),
        FieldPanel('bio'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class NewsPage(Page):
    parent_page_types = ['home.HomePage']

    # db
    authors = ParentalManyToManyField(
        Author,
        blank=True,
        related_name='news_pages',
        verbose_name='Авторы',
    )

    # user input
    content_panels = Page.content_panels + [
        FieldPanel('authors'),
    ]


class HomePage(Page):
    subpage_types = ['home.NewsPage']

    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['latest_news'] = (
            NewsPage.objects
            .live()
            .child_of(self)
            .order_by('-first_published_at')[:3]
        )
        return context

    # db
    subtitle = models.TextField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Подзаголовок'
    )

    rtfblock = RichTextField(
        null=True,
        blank=True,
        features=['h1', 'bold', 'italic', 'link', 'ol', 'ul'],
    )

    # user input
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('rtfblock'),
    ]
