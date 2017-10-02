from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, String, Nested, Integer, \
                              analyzer, tokenizer
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

connections.create_connection(update_all_types=True)

def comp_analyzer = analyzer('comp_analyzer',
        tokenizer=tokenizer('gram', 'edge_ngram', min_gram=2, max_gram=15))

class RecipeIndex(DocType):
    author = String()
    likes = Integer()
    title = String()
    description = Text()
    ingredients = Nested(properties={'name': String(),
                                     'measure': String()})
    created_at = Date()
    updated_at = Date()

    class Meta:
        index = 'recipe_index'


def bulk_indexing():
    from .models import Recipe
    RecipeIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in
                             Recipe.objects.all().iterator()))


def multi_search(text):
    es = Elasticsearch()
    body = []
    index = {'index': 'recipe_index', 'type': 'recipe_index'}
    search_ings = {'query':
                   {'nested':
                    {'path': 'ingredients', 'query':
                     {'match': {'ingredients.name':
                                {'fuzziness': 1, 'query': text}}}}}}
    search_recipe = {'query': {'multi_match':
                     {'fields': ['title', 'description'],
                      'query': text, 'fuzziness': 1}}}
    body.extend([index, search_ings, index, search_recipe])
    return es.msearch(body=body)


def list_recipes(response):
    hits = [i['hits']['hits'] for i in response['responses']]
    recipes = []
    for array in hits:
        for item in array:
            recipes.append(item)
    return recipes


def sort_by_likes(recipe_list):
    return sorted(recipe_list, key=lambda d: d['_source']['likes'],
                  reverse=True)


def get_recipes_from_es(q):
    response = multi_search(q)
    recipes = list_recipes(response)
    if recipes:
        print('recipes loaded')
        recipes = sort_by_likes(recipes)
        # get rid of underscores
        for recipe in recipes:
            recipe['id'] = recipe.pop('_id')
            recipe['source'] = recipe.pop('_source')
        return recipes
    return None
