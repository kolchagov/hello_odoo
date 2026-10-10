from odoo.exceptions import UserError
from odoo.addons.base.tests.common import BaseCommon


class TestHelloGreeting(BaseCommon):
    def test_app_menu_opens_greeting_form(self):
        root_menu = self.env.ref("hello_odoo.hello_odoo_menu_root")
        greeting_menu = self.env.ref("hello_odoo.hello_greeting_menu")

        self.assertFalse(root_menu.parent_id)
        self.assertEqual(greeting_menu.parent_id, root_menu)
        action = greeting_menu.sudo().action
        self.assertEqual(action.res_model, "hello.greeting")
        self.assertEqual(action.view_mode, "form")

    def test_say_hello_strips_username(self):
        greeting = self.env["hello.greeting"].create({"username": "  Ada  "})

        greeting.action_say_hello()

        self.assertEqual(greeting.username, "Ada")
        self.assertEqual(greeting.greeting, "Hello Ada from Odoo 20")

    def test_say_hello_rejects_blank_username(self):
        greeting = self.env["hello.greeting"].create({"username": "   "})

        with self.assertRaises(UserError):
            greeting.action_say_hello()
