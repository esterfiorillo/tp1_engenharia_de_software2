from unittest import skip
from django.test import TestCase
from api.views import RecipesViewSet
from django.test import Client
import json

#testes de integração do sistema, dependem de views, elastic_queries,filter_utils e da base de dados
#O teste está comentado pois não conseguimos fazer ele funcionar no github actions devido ao elastic search
@skip('Integration test')
class SearchesTestCase(TestCase):
    def setUp(self):
       self.client = Client()

    def test_search_ingredient(self):
        response=self.client.get('/recipes/search/?ingredients=ovo')
        documents = json.loads(response.content)
        #checar se retornou pelo menos uma receita
        self.assertGreater(len(documents),0)
        #checar se a receitas são adequadas
        for line in documents:
            self.assertIn('ovo',line['raw_text'])

    def test_search_name(self):
        response=self.client.get('/recipes/search/?name=bolo')
        documents = json.loads(response.content)
        #checar se retornou pelo menos uma receita
        self.assertGreater(len(documents),0)
        #checar se a receitas são adequadas
        for line in documents:
            self.assertIn('bolo',line['raw_text'])

    def test_search_title(self):
        response=self.client.get('/recipes/search/?title=bolo')
        documents = json.loads(response.content)
        #checar se retornou pelo menos uma receita
        self.assertGreater(len(documents),0)
        #checar se a receitas são adequadas
        for line in documents:
            self.assertIn('bolo',line['raw_text'])

    def test_search_multiple_ingredients(self):
        response=self.client.get('/recipes/search/?ingredients=ovo&leite')
        documents = json.loads(response.content)
        #checar se retornou pelo menos uma receita
        self.assertGreater(len(documents),0)
        #checar se a receitas são adequadas
        for line in documents:
            self.assertIn('ovo',line['raw_text'])
            self.assertIn('leite',line['raw_text'])

    def test_search_for_nothing(self):
        response=self.client.get('recipes/search/?')
        self.assertEqual(response.status_code, 404)
