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

    def test_start_retrieve_list(self):
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

        # User confirms that the site has generated a unique url

        # User visits the unique url and confirms items are still shown
        self.fail('Finish the tests')
