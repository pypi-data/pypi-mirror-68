from datetime import datetime
from typing import Optional
from typing import Union

from aldryn_search.search_indexes import TitleIndex
from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from cms.models import Title
from cms.test_utils.testcases import BaseCMSTestCase
from cms.toolbar.toolbar import CMSToolbar
from django.conf import settings
from django.db.models import QuerySet
from django.forms import Media
from django.http import HttpRequest
from django.test import Client
from haystack.indexes import SearchIndex


class FakeCMSRequestFactor(BaseCMSTestCase):
    client = Client
    
    def get_request(self, *args, **kwargs) -> HttpRequest:
        request = super().get_request(*args, **kwargs)
        request.placeholder_media = Media()
        request.session = {}
        request.toolbar = CMSToolbar(request)
        return request


class AlgoliaPageDataProxy(Title):

    class Meta:
        proxy = True

    def page_content(self) -> str:
        aldryn_haystack_index: Union[SearchIndex, TitleIndex] = TitleIndex()
        return aldryn_haystack_index.get_search_data(
            obj=self,
            language=settings.LANGUAGE_CODE,
            request=FakeCMSRequestFactor().get_request(),
        )

    def pub_date(self) -> datetime:
        return self.page.publication_date

    def url(self) -> datetime:
        return self.page.get_absolute_url()
    
    def description(self) -> Optional[str]:
        return self.meta_description


@register(AlgoliaPageDataProxy)
class PageIndex(AlgoliaIndex):
    index_name = 'pages'
    
    fields = [
        'title',
        'url',
        'pub_date',
        'description',
        'page_content',
    ]

    def get_queryset(self) -> QuerySet:
        aldryn_haystack_index: SearchIndex = TitleIndex()
        return aldryn_haystack_index.get_index_queryset(
            language=settings.LANGUAGE_CODE,
        )
