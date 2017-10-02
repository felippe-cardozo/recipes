import json
import requests
from .models import Recipe, Measure


data = {
        "settings": {
            "number_of_shards": 4,
            "number_of_replicas": 1
            },
        "mappings": {
            "recipe": {
                "properties": {
                    "title": {"type": "text", "boost": 4},
                    "description": {"type": "text", "boost": 3},
                    "likes": {"type": "text"},
                    "author": {"type": "text"},
                    "ings": {"type": "text", "boost": 2},
                    "created_at": {"type": "text"},
                    "updated_at": {"type": "text"}
                    }
                }
            }
        }


def setup_index(data=data, name='recipe_index'):
    url = 'http://localhost:9200/recipe_index'.format(name)
    response = requests.put(url, data=json.dumps(data))
    return response


def feed_index():
    data = ''
    for r in Recipe.objects.all():
        data += '{"index": {"_id": "%s"}}\n' % r.pk
        ingredients = {}
        for i in r.measure_set.all():
            ingredients[i.ingredient.name] = i.measure
        data += json.dumps({
            "title": r.title,
            "description": r.description,
            "likes": r.likes.count(),
            "author": r.author.username,
            "ingredients": ingredients,
            "created_at": str(r.created_at),
            "updated_at": str(r.updated_at),
            }) + '\n'
        response = requests.put('http://localhost:9200/recipe_index/recipes/_bulk',
                                data=data)
        return response
