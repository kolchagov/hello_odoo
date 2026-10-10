import re

from odoo.tests import HttpCase


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
        self.assertIn("Hello &lt;Ada&gt; from Odoo 20", greeting.text)
