import sys
import os
import unittest

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from new8thmodule.pages.input_page import InputPage


class TestInputPage(InputPage):
    def setUp(self, driver):
        super().__init__(driver)

    def test_add_text(self):
        self.add_text('HOO')

    def test_show_message(self):
        self.show_message('HOO')


if __name__ == "__main__":
    unittest.main()
