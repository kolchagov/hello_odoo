from odoo import fields, models
from odoo.exceptions import UserError


class HelloGreeting(models.TransientModel):
    _name = "hello.greeting"
    _description = "Hello greeting"

    username = fields.Char(required=True, size=80)
    greeting = fields.Char(readonly=True)

    def action_say_hello(self):
        self.ensure_one()
        username = (self.username or "").strip()
        if not username:
            raise UserError(self.env._("Please enter a username."))
        if len(username) > 80:
            raise UserError(self.env._("Username must be 80 characters or fewer."))
        self.write({
            "username": username,
            "greeting": self.env._("Hello %s from Odoo 20", username),
        })
