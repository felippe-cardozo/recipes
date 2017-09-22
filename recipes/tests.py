from django.test import TestCase, Client
from django.contrib.auth.models import User
from recipes.models import Recipe, Ingredient, Measure
from recipes.forms import RecipeForm, IngredientFormSet


class RecipeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='password')
        self.lasanha = Recipe(title='lasanha', description='placeholder',
                              author=self.user)
        self.macarrao = Recipe(title='macarrao', description='placeholder',
                               author=self.user)
        self.batata = Ingredient(name='batata')
        self.molho = Ingredient(name='molho')

    def test_recipe_is_saved(self):
        self.lasanha.save()
        self.macarrao.save()
        self.assertEqual('lasanha', Recipe.objects.all()[0].title)

    def test_update_ingredients_method(self):
        self.lasanha.save()
        self.batata.save()
        self.molho.save()
        Measure.objects.create(recipe=self.lasanha,
                               ingredient=self.batata,
                               measure='duas')
        new_ingredients = {'batata': 'uma', 'molho': 'um'}
        new_ingredients2 = {'cenoura': 'uma'}
        self.lasanha.update_ingredients(new_ingredients)
        self.assertEqual(self.lasanha.measure_set.all().count(), 2)
        self.assertEqual(self.lasanha.measure_set.get(
                         ingredient=self.batata).measure, 'uma')
        self.assertEqual(self.lasanha.measure_set.get(
            ingredient=Ingredient.objects.get(name='molho')
            ).measure, 'um')
        self.lasanha.update_ingredients(new_ingredients2)
        self.assertEqual(self.lasanha.ingredients.count(), 1)
        self.assertEqual(self.lasanha.measure_set.get(
            ingredient=Ingredient.objects.get(name='cenoura')
            ).measure, 'uma')


class IngredientModelTest(TestCase):
    def setUp(self):
        self.batata = Ingredient(name='batata')
        self.cenoura = Ingredient(name='cenoura')

    def test_ingredient_is_saved(self):
        self.batata.save()
        self.assertEqual(Ingredient.objects.all()[0].name, 'batata')


class MeasureRelationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='password')
        self.lasanha = Recipe(title='lasanha', description='placeholder',
                              author=self.user)
        self.batata = Ingredient(name='batata')

    def test_create_association(self):
        self.lasanha.save()
        self.batata.save()
        Measure(ingredient=self.batata, recipe=self.lasanha,
                measure='1 kilo').save()
        batata_lasanha = Measure.objects.get(ingredient=self.batata,
                                             recipe=self.lasanha)
        self.assertEqual(self.lasanha.ingredients.all()[0].name, 'batata')
        self.assertEqual(batata_lasanha.measure, '1 kilo')


class RecipeFormTest(TestCase):
    def setUp(self):
        self.data = {'title': 'lasanha', 'description': 'placeholder'}

    def test_form_is_valid(self):
        form = RecipeForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid(self):
        self.data['title'] = ''
        form = RecipeForm(data=self.data)
        self.assertFalse(form.is_valid())


class IngredientFormSetTest(TestCase):
    def setUp(self):
        self.formset = IngredientFormSet
        self.data = {
                'form-TOTAL_FORMS': '2',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
                'form-0-name': 'batata',
                'form-0-measure': '1 kilo',
                'form-1-name': 'banana',
                'form-1-measure': '2 kilos'}

    def test_formset_is_valid(self):
        formset = self.formset(data=self.data)
        self.assertTrue(formset.is_valid())

    def test_formset_is_invalid(self):
        self.data['form-0-name'] = ''
        self.data['form-1-name'] = ''
        formset = self.formset(data=self.data)
        self.assertFalse(formset.is_valid())


class ViewsTest(TestCase):

    fixtures = ['users.json']

    def setUp(self):
        self.user = User.objects.create_user(username='user',
                                             password='password')
        self.recipe = Recipe.objects.create(title='test',
                                            description='placeholder',
                                            author=self.user)
        self.data = {
                     'title': 'Test',
                     'description': 'desc',
                     'form-TOTAL_FORMS': '2',
                     'form-INITIAL_FORMS': '0',
                     'form-MAX_NUM_FORMS': '',
                     'form-0-name': 'batata',
                     'form-0-measure': '1 kilo',
                     'form-1-name': 'banana',
                     'form-1-measure': '2 kilos'}

    def test_post_new_recipe_with_ingredients(self):
        c = Client()
        c.login(username='user', password='password')
        response = c.post('/recipes/new', self.data)
        self.assertEqual(response.status_code, 302)
        recipe = Recipe.objects.last()
        self.assertEqual(Recipe.objects.last().title, 'Test')
        self.assertEqual(recipe.ingredients.count(), 2)
        recipe = Recipe.objects.get(title='Test')
        ingredient = Ingredient.objects.get(name='batata')
        assoc = Measure.objects.get(ingredient=ingredient, recipe=recipe)
        self.assertEqual(assoc.measure, '1 kilo')

    def test_update_recipe(self):
        c = Client()
        recipe = Recipe.objects.create(title='test', description='test',
                                       author=self.user)
        update_url = '/recipes/update/' + str(recipe.id) + '/'
        batata = Ingredient.objects.create(name='batata')
        cenoura = Ingredient.objects.create(name='cenoura')
        recipe.measure_set.create(ingredient=batata, measure='duas')
        recipe.measure_set.create(ingredient=cenoura, measure='duas')
        response = c.get(update_url)
        self.assertEqual(response.status_code, 200)
        form = response.context.get('form')
        recipe_data = form.initial
        formset = response.context['formset']
        ingredients_data = formset.initial
        self.assertEqual(recipe_data['title'], 'test')
        self.assertTrue(ingredients_data[0]['name'] in {'batata', 'cenoura'})

    def test_index_page(self):
        c = Client()
        response = c.get('/recipes/')
        self.assertEqual(response.status_code, 200)

    def test_detail_view(self):
        recipe = Recipe.objects.create(title='test', description='test',
                                       author=self.user)
        c = Client()
        response = c.get('/recipes/' + str(recipe.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        c = Client()
        response = c.post('/login/', {'username': 'fcc',
                                      'password': 'password'})
        self.assertEqual(response.status_code, 302)

    def test_registration_view(self):
        c = Client()
        data = {'username': 'testuser', 'email': 'test@gmail.com',
                'password': 'password', 'confirm_password': 'password'}
        response = c.post('/registration/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.last().username, 'testuser')

    def test_like_and_unlike_view(self):
        c = Client()
        c.login(username='f', password='password')
        c.post('/recipes/like/' + str(self.recipe.id) + '/')
        self.assertEqual(self.recipe.likes.count(), 1)
        c.post('/recipes/unlike/' + str(self.recipe.id) + '/')
        self.assertEqual(self.recipe.likes.count(), 0)

    def test_add_and_remove_from_cookbook(self):
        c = Client()
        c.login(username='f', password='password')
        c.post('/recipes/add_to_cookbook/' + str(self.recipe.id) + '/')
        self.assertEqual(self.recipe.cookbook_users.count(), 1)
