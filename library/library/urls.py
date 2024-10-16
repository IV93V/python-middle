"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework import routers
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from books.views import EditionKindsViewSet, BookViewSet
from person.views import AgentsViewSet, AuthorViewSet, LibrarierViewSet
from reader_cards.views import ReaderCardBooksViewSet, ReaderCardsViewSet
from library_structure.views import HallsViewSet, RacksViewSet, ShelfViewSet
from books_move_journal.views import BookMoveJournalViewSet, BookMoveJournalActionsViewSet

router = routers.DefaultRouter()

router.register(r'edition_kinds', EditionKindsViewSet)
router.register(r'agents', AgentsViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'librariers',LibrarierViewSet)
router.register(r'halls', HallsViewSet)
router.register(r'racks', RacksViewSet)
router.register(r'shelfs',ShelfViewSet)
router.register(r'books',BookViewSet)
router.register(r'reader_cards',ReaderCardsViewSet)
router.register(r'reader_card_books',ReaderCardBooksViewSet)
router.register(r'movement_journal',BookMoveJournalViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version='v1',
        description="Library API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    )
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('swagger<format>/',schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/',schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),
]
