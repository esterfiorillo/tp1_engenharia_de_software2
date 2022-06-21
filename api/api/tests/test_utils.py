from django.test import TestCase

from api.filters_utils import FilterUtils

class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def test_generate_filters_no_param(self):
        """Test the generate_filters function with no parameters."""
        params = {}
        filters = None
        self.assertEqual(
            FilterUtils.generate_filters(params),
            filters)
        
    def test_generate_filters_all_params(self):
        """Test the generate_filters function with all parameters."""
        params = {
            'group': 'sopas',
            'time_min': 1,
            'time_max': 2,
            'portions_min': 3,
            'portions_max': 4,
            'favorites_min': 5,
            'favorites_max': 6,
        }
        filters = {
            'group': ['Sopas'],
            'preparation_time': (1, 2),
            'portions': (3, 4),
            'favorites': (5, 6)
        }
        self.assertEqual(
            FilterUtils.generate_filters(params),
            filters)

    def test_get_query_by_name_without_filters(self):
        must = [
            {
                "multi_match": {
                    "query": 'bolo de limão',
                    "fields": [
                        "recipe_title^2",
                        "ingredients^2",
                        "raw_text"
                    ],
                    "type": "most_fields",
                    "fuzziness": 1
                }
            }
        ]
        query = {
            "query": {
                "bool": {
                    "must": must
                }
            }
        }
        self.assertEqual(FilterUtils.get_query_by_name_filtred('bolo de limão', filters=None, fuzziness=1),
                        query)

    def test_get_query_by_name_with_filters(self):
        must = [
            {
                "multi_match": {
                    "query": 'bolo de limão',
                    "fields": [
                        "recipe_title^2",
                        "ingredients^2",
                        "raw_text"
                    ],
                    "type": "most_fields",
                    "fuzziness": 1
                }
            }
        ]
        filters = {
            'group': ['Bolos'],
            'preparation_time': (1, 2),
            'portions': (3, 4),
            'favorites': (5, 6)
        }
        must = must + FilterUtils.get_filter_queries(filters)
        query = {
            "query": {
                "bool": {
                    "must": must
                }
            }
        }
        self.assertEqual(FilterUtils.get_query_by_name_filtred('bolo de limão', filters={
                        'group': ['Bolos'],
                        'preparation_time': (1, 2),
                        'portions': (3, 4),
                        'favorites': (5, 6)
                        }, fuzziness=1),
                            query)

    def test_get_query_by_ingredients_without_filters(self):
        ingredients = ['farinha', 'ovo']
        must = [
            {
                "match": {
                    "ingredients": {
                        "query": ingredient,
                        "fuzziness": 1
                    },
                }
            } for ingredient in ingredients
        ]
        query = {
            "query": {
                "bool": {
                    "must": must
                }
            }
        }
        self.assertEqual(FilterUtils.get_query_by_ingredients_filtred(['farinha', 'ovo'], filters=None, fuzziness=1),
                         query)

    def test_get_query_by_ingredients_with_filters(self):
        ingredients = ['tomate', 'alface']
        must = [
            {
                "match": {
                    "ingredients": {
                        "query": ingredient,
                        "fuzziness": 1
                    },
                }
            } for ingredient in ingredients
        ]
        filters = {
            'group': ['Saladas'],
            'preparation_time': (1, 2),
            'portions': (3, 4),
            'favorites': (5, 6)
        }
        must = must + FilterUtils.get_filter_queries(filters)
        query = {
            "query": {
                "bool": {
                    "must": must
                }
            }
        }
        self.assertEqual(FilterUtils.get_query_by_ingredients_filtred(['tomate', 'alface'], filters={
                        'group': ['Saladas'],
                        'preparation_time': (1, 2),
                        'portions': (3, 4),
                        'favorites': (5, 6)
                        }, fuzziness=1),
                        query)