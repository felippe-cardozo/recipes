from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, String, Nested, Integer, \
        Completion
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

connections.create_connection(update_all_types=True)


class RecipeIndex(DocType):
    author = String()
    likes = Integer()
    title = String()
    description = Text()
    ingredients = Nested(properties={'name': String(),
                                     'measure': String()})
    image = String()
    tags = Completion()
    created_at = Date()
    updated_at = Date()

    class Meta:
        index = 'recipe_index'


def bulk_indexing():
    es = Elasticsearch()
    if es.indices.exists(index='recipe_index'):
        es.indices.delete(index='recipe_index')
    from .models import Recipe
    RecipeIndex.init()
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
    response = es.msearch(body=body)
    return response


def list_recipes(response):
    hits = [i['hits']['hits'] for i in response['responses']]
    recipes = []
    ids = []
    for array in hits:
        for item in array:
            if item['_id'] not in ids:
                ids.append(item['_id'])
                recipes.append(item)
    return recipes


def sort_by_likes(recipe_list):
    return sorted(recipe_list, key=lambda d: (d['_score'],
                                              d['_source']['likes']),
                  reverse=True)


def get_recipes_from_es(q):
    response = multi_search(q)
    recipes = list_recipes(response)
    if recipes:
        recipes = sort_by_likes(recipes)
        # get rid of underscores
        for recipe in recipes:
            recipe['id'] = recipe.pop('_id')
            recipe['source'] = recipe.pop('_source')
        return recipes
    return None


def suggestions(text, index='recipe_index'):
    es = Elasticsearch()
    body = {'suggest': {'recipe_index_suggest':
                        {'text': text,
                         'completion': {'field': 'tags'}}}}
    return es.search(index=index, body=body)


# takes suggestions object as input and returns a list of words
def list_suggestions(suggestions):
    options = suggestions['suggest']['recipe_index_suggest'][0]['options']
    return list({i['text'] for i in options})


def get_suggestions_from_es(q):
    s = suggestions(q)
    return list_suggestions(s)
