from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_start_retrieve_list(self):
        # User navigates to to-do list homepage
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy test item 1' for row in rows),
            'New to-do item did not appear in table'
        )

        # User is still presented with a prompt to add a to-do item
        self.fail('Finish test tests')

        # User types 'Buy test item 2' into a text box

        # User presses enter, the page now lists both items

        # User confirms that the site has generated a unique url

        # User visits the unique url and confirms items are still shown


if __name__ == '__main__':
    unittest.main(warnings='ignore')