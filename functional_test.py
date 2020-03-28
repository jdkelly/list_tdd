from selenium import webdriver
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
        self.fail('Finish the test')

        # User is invited to enter a to-do item immediately

        # User types 'Buy test item 1' into a text box

        # User presses enter, the page now lists '1: Buy test item 1'

        # User is still presented with a prompt to add a to-do item

        # User types 'Buy test item 2' into a text box

        # User presses enter, the page now lists both items

        # User confirms that the site has generated a unique url

        # User visits the unique url and confirms items are still shown


if __name__ == '__main__':
    unittest.main(warnings='ignore')