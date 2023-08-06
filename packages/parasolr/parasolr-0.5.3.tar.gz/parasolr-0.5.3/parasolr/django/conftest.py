try:
    import django
except ImportError:
    django = None

import pytest

if django:

    from parasolr.django import SolrClient

    @pytest.fixture
    def empty_solr():
        # pytest solr fixture; updates solr schema
        SolrClient().update.delete_by_query('*:*')
