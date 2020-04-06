from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # User navigates to to-do list homepage
        self.browser.get(self.live_server_url)

        # User checks 'to-do lists' are in the page title
        self.assertIn('To-Do lists', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User is invited to enter a to-do item immediately
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEquals(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # User types 'Buy test item 1' into a text box
        input_box.send_keys('Buy test item 1')

        # User presses enter, the page now lists '1: Buy test item 1'
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy test item 1')

        # User is still presented with a prompt to add a to-do item
        # User types 'Buy test item 2' into a text box
        # User presses enter, the page now lists both items
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy test item 2')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy test item 1')
        self.wait_for_row_in_list_table('2: Buy test item 2')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy test item 1')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy test item 1')

        # Edith notices the list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # A new user, Francis, come to the site

        ## A new browser session is used
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the homepage. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy test item 1', page_text)
        self.assertNotIn('Buy test item 2', page_text)

        # Francis starts a new list by entering a new item
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets a unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy test item 1', page_text)
        self.assertIn('Buy milk', page_text)

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )

        # She starts a new list and sees the input still centered
        input_box.send_keys('testing')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )

