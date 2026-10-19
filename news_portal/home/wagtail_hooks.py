from wagtail import hooks
from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.admin.ui.tables import Column

from .models import NewsPage


class NewsPageListingViewSet(PageListingViewSet):
    model = NewsPage
    icon = "doc-full"
    menu_label = "Новости"
    add_to_admin_menu = True
    menu_order = 200

    columns = PageListingViewSet.columns + [
        Column("first_published_at", label="Дата", sort_key="first_published_at"),
    ]


news_page_listing_viewset = NewsPageListingViewSet("news_pages")


@hooks.register("register_admin_viewset")
def register_news_page_listing_viewset():
    return news_page_listing_viewset
