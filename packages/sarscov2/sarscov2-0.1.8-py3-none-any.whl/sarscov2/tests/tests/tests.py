from django.test import TestCase, tag
from model_bakery.baker import make_recipe


class TestCoranavirus(TestCase):
    def test_(self):
        obj = make_recipe("sarscov2.tests.coronaviruskap")
