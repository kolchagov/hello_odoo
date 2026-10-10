import re
from html.parser import HTMLParser

from odoo.tests import HttpCase


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)


class TestHelloPage(HttpCase):
    def test_username_greeting_and_empty_username_error(self):
        page = self.url_open("/hello_odoo")
        csrf_token = re.search(r'name="csrf_token" value="([^"]+)"', page.text)
        assert csrf_token is not None

        empty_response = self.url_open(
            "/hello_odoo",
            data={"csrf_token": csrf_token.group(1), "username": ""},
        )
        self.assertIn("Please enter a username.", empty_response.text)

        csrf_token = re.search(
            r'name="csrf_token" value="([^"]+)"', empty_response.text
        )
        assert csrf_token is not None
        greeting = self.url_open(
            "/hello_odoo",
            data={"csrf_token": csrf_token.group(1), "username": "<Ada>"},
        )
        visible_text = TextParser()
        visible_text.feed(greeting.text)
        self.assertIn("Hello <Ada> from Odoo 20", "".join(visible_text.text))
        self.assertIn("&lt;Ada&gt;", greeting.text)
