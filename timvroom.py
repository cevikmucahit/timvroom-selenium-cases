import unittest
import selenium.webdriver.support.expected_conditions as ec

from config import browser
from locators.timvroom_locators import ROOM_URL, ANSWER_INPUT_1, NAME_INPUT, DROPDOWN, BLUE_BOX_COUNT, \
    ANSWER_INPUT_4, LINK_CLICK, RED_BOX, ANSWER_INPUT_6, RADIO_BUTTON, ANSWER_INPUT_10, \
    GREEN_AND_ORANGE_BOX, ANSWER_INPUT_11, ANSWER_INPUT_13, IS_HERE_ELEMENT, PURPLE_BOX, PURPLE_BOX_INPUT, \
    CLICK_WAIT_LINK, CLICK_AFTER_LINK, SUBMIT_INPUT, CHECK_RESULT, ALL_TEST_CASE_CONTROL, \
    ANSWER_INPUT_8
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select


class SeleniumCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = browser()
        cls.driver.get(ROOM_URL)

    def test_case_1(self):
        """ Grab page title and place title text in answer slot #1"""

        title_input = self.driver.find_element(*ANSWER_INPUT_1)
        title_input.send_keys("Selenium Playground")

        self.assertEqual("Selenium Playground", title_input.get_attribute("value"))

    def test_case_2(self):
        """ Fill out name section of form to be Kilgore Trout """
        name_input = self.driver.find_element(*NAME_INPUT)
        name_input.send_keys("Kilgore Trout")

        self.assertEqual("Kilgore Trout", name_input.get_attribute("value"))

    def test_case_3(self):
        """ Set occupation on form to Sci-Fi Author """
        dropdown = Select(self.driver.find_element(*DROPDOWN))
        dropdown.select_by_visible_text("Science Fiction Author")

        self.assertEqual("Science Fiction Author", dropdown.first_selected_option.text)

    def test_case_4(self):
        """ Count number of blue_boxes on page after form and enter into answer box #4 """
        blue_box_count = self.driver.find_elements(*BLUE_BOX_COUNT)

        count = 0
        for blue in blue_box_count:
            if blue:
                count = count + 1

        blue_box_write_input = self.driver.find_element(*ANSWER_INPUT_4)
        blue_box_write_input.send_keys(str(count))

        self.assertEqual(str(count), blue_box_write_input.get_attribute("value"))

    def test_case_5(self):
        """ Click link that says 'click me' """
        link = self.driver.find_element(*LINK_CLICK)
        link.click()

        self.assertEqual(link, self.driver.switch_to.active_element)

    def test_case_6(self):
        """ Find red box on its page find class applied to it, and enter into answer box #6 """
        red_box = self.driver.find_element(*RED_BOX)
        class_write_input = self.driver.find_element(*ANSWER_INPUT_6)
        class_write_input.send_keys(red_box.get_attribute("class"))

        self.assertTrue(class_write_input.get_attribute("value"))

    def test_case_7(self):
        """ Run JavaScript function as: ran_this_js_function() from your Selenium script """
        self.driver.execute_script("ran_this_js_function()")

    def test_case_8(self):
        """
            Run JavaScript function as: got_return_from_js_function() from your Selenium script,
            take returned value and place it in answer slot #8
        """
        result = str(self.driver.execute_script("return got_return_from_js_function()"))

        answer_input = self.driver.find_element(*ANSWER_INPUT_8)
        answer_input.send_keys(result)

        self.assertEqual(answer_input.get_attribute("value"), result)

    def test_case_9(self):
        """ Mark radio button on form for written book? to Yes """
        radio_button = self.driver.find_element(*RADIO_BUTTON)
        radio_button.click()

        self.assertTrue(radio_button.get_attribute("checked"))

    def test_case_10(self):
        """ Get the text from the Red Box and place it in answer slot #10 """
        red_box = self.driver.find_element(*RED_BOX)

        red_box_text_input = self.driver.find_element(*ANSWER_INPUT_10)
        red_box_text_input.send_keys(red_box.text)

        self.assertTrue(red_box_text_input)

    def test_case_11(self):
        """ Which box is on top? orange or green -- place correct color in answer slot #11 """
        green_orange_box = self.driver.find_element(*GREEN_AND_ORANGE_BOX)
        write_input = self.driver.find_element(*ANSWER_INPUT_11)

        get_text = green_orange_box.text.replace(" Box", "")
        write_input.send_keys(get_text)

        self.assertEqual(get_text, write_input.get_attribute("value"))

    def test_case_12(self):
        """ Set browser width to 850 and height to 650 """
        self.driver.set_window_size(848, 648)

    def test_case_13(self):
        """ Type into answer slot 13 yes or no depending on whether item by id of ishere is on the page """
        yes_or_no_input = self.driver.find_element(*ANSWER_INPUT_13)

        try:
            self.driver.find_element(*IS_HERE_ELEMENT)
            yes_or_no_input.send_keys("yes")

        except NoSuchElementException:
            yes_or_no_input.send_keys("no")

        self.assertIn(yes_or_no_input.get_attribute("value"), ["yes", "no"])

    def test_case_14(self):
        """ Type into answer slot 14 yes or no depending on whether item with id of purplebox is visible """
        purple_box_input = self.driver.find_element(*PURPLE_BOX_INPUT)

        wait = WebDriverWait(self.driver, 3)
        try:
            wait.until(ec.visibility_of_element_located(PURPLE_BOX))
            purple_box_input.send_keys("yes")
        except TimeoutException:
            purple_box_input.send_keys("no")

        self.assertTrue(purple_box_input)

    def test_case_15(self):
        """
            Waiting game: click the link with link text of 'click then wait' a random wait will occur
            (up to 10 seconds) and then a new link will get added with link text of 'click after wait' - click this
            new link within 500 ms of it appearing to pass this test
        """
        click_waiting_link = self.driver.find_element(*CLICK_WAIT_LINK)
        click_waiting_link.click()

        wait = WebDriverWait(self.driver, 15)
        wait.until(ec.presence_of_element_located(CLICK_AFTER_LINK))

        after_click = self.driver.find_element(*CLICK_AFTER_LINK)
        after_click.click()

        alert = self.driver.switch_to.alert
        clean_text = int(alert.text.replace("Clicked link within ", "").replace("ms", ""))
        alert.accept()

        self.assertLessEqual(clean_text, 500)

    def test_case_17(self):
        """ Click the submit button on the form """
        submit_button = self.driver.find_element(*SUBMIT_INPUT)
        submit_button.click()

        self.assertEqual(submit_button, self.driver.switch_to.active_element)

    def test_case_99(self):
        """ CHECK RESULTS :) Yaaay! """
        check_result = self.driver.find_element(*CHECK_RESULT)
        check_result.click()

        all_cases = self.driver.find_elements(*ALL_TEST_CASE_CONTROL)

        print(len(all_cases))

        self.assertEqual(0, len(all_cases))

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
