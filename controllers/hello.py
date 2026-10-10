from odoo import http
from odoo.http import request


class HelloOdoo(http.Controller):
    @http.route(
        "/hello_odoo",
        type="http",
        auth="public",
        methods=["GET", "POST"],
        csrf=True,
    )
    def index(self):
        submitted = request.httprequest.method == "POST"
        username = request.httprequest.form.get("username", "").strip() if submitted else ""
        error = False

        if submitted and not username:
            error = request.env._("Please enter a username.")
        elif len(username) > 80:
            error = request.env._("Username must be 80 characters or fewer.")

        return request.render(
            "hello_odoo.hello_odoo_page",
            {"error": error, "submitted": submitted, "username": username},
        )
