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

    def test_save_displays_greeting(self):
        greeting = self.env["hello.greeting"].create({"username": "  Ada  "})

        self.assertEqual(greeting.username, "Ada")
        self.assertEqual(greeting.greeting, "Greetings from Odoo, Ada")

    def test_saving_username_updates_greeting(self):
        greeting = self.env["hello.greeting"].create({"username": "Ada"})
        greeting.write({"username": " Grace "})

        self.assertEqual(greeting.username, "Grace")
        self.assertEqual(greeting.greeting, "Greetings from Odoo, Grace")

    def test_save_rejects_blank_username(self):
        with self.assertRaises(UserError):
            self.env["hello.greeting"].create({"username": "   "})
