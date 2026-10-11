from odoo import api, fields, models
from odoo.exceptions import UserError


class HelloGreeting(models.TransientModel):
    _name = "hello.greeting"
    _description = "Hello greeting"

    username = fields.Char(required=True, size=80)
    greeting = fields.Char(readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [self._prepare_greeting_values(vals) for vals in vals_list]
        return super().create(vals_list)

    def write(self, vals):
        if "username" in vals:
            vals = self._prepare_greeting_values(vals)
        return super().write(vals)

    def _prepare_greeting_values(self, vals):
        vals = vals.copy()
        username = (vals.get("username") or "").strip()
        if not username:
            raise UserError(self.env._("Please enter a username."))
        if len(username) > 80:
            raise UserError(self.env._("Username must be 80 characters or fewer."))
        vals.update(
            username=username,
            greeting=self.env._("Greetings from Odoo, %s", username),
        )
        return vals
