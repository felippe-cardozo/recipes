from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['recipes/fixtures/users.json', 'recipes/fixtures/recipes.json']

    @classmethod
    def setUpClass(cls):
        super(MySeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('fcc')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('password')
        self.selenium.find_element_by_xpath('//input[@value="Login"]').click()

    def test_login(self):
        self.login()
        self.assertIn('Index', self.selenium.title)

    def test_update_recipe(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/recipes'))
        details = self.selenium.find_elements_by_link_text('View More')
        details[0].click()
        update_link = self.selenium.find_elements_by_link_text('Update')
        update_link[0].click()
        ingredient_name = self.selenium.find_elements_by_name('form-3-name')
        ingredient_name[0].click()
        ingredient_name[0].send_keys('Batata Doce')
        measure = self.selenium.find_elements_by_name('form-3-measure')
        measure[0].send_keys('um kilo')
        measure[0].send_keys(Keys.ENTER)
        ingredients = self.selenium.find_elements_by_id('ingredient')
        self.assertTrue(any(i.text == 'Batata Doce um kilo'
                            for i in ingredients))

    def test_like_recipe(self):
        self.login()
        details = self.selenium.find_elements_by_link_text('View More')
        details[2].click()
        likes_count = self.selenium.find_element_by_id('likes_count').text
        like = self.selenium.find_elements_by_id('like')
        like[0].click()
        new_likes_count = self.selenium.find_element_by_id('likes_count').text
        self.assertEqual(int(new_likes_count) - int(likes_count), 1)
        unlike = self.selenium.find_elements_by_id('unlike')
        unlike[0].click()
        likes_count = new_likes_count
        new_likes_count = self.selenium.find_element_by_id('likes_count').text
        self.assertEqual(int(new_likes_count) - int(likes_count), -1)

    def test_add_to_cookbook(self):
        self.login()
        details = self.selenium.find_elements_by_link_text('View More')
        details[0].click()
        add_to_cookbook = self.selenium.find_elements_by_id('add_cookbook')
        add_to_cookbook[0].click()
        remove_from_cookbook = self.selenium.find_elements_by_id(
                'remove_cookbook')
        self.assertTrue(remove_from_cookbook)
