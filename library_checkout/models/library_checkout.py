# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions


class Checkout(models.Model):
    _name = 'library.checkout'
    _description = "Checkout Request"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.depends('member_id')
    def _compute_request_date_onchange(self):
        today_date = fields.Date.today()
        if self.request_date != today_date:
            self.request_date = today_date
            return {
                'warning': {
                    'title': "Change Request Date",
                    'message': 'Request date changed to today'
                }
            }

    @api.model
    def _default_stage_id(self):
        Stage = self.env["library.checkout.stage"]
        return Stage.search([("state", "=", "new")], limit=1)

    @api.model
    def _group_expand_stage_id(self, stages, domain, order):
        return stages.search([], order=order)

    name = fields.Char(string="Title")
    member_image = fields.Binary(related="member_id.image_128")
    member_id = fields.Many2one(
        "library.member",
        required=True,
    )
    user_id = fields.Many2one(
        "res.users",
        "Librarian",
        default=lambda s: s.env.user,
    )
    request_date = fields.Date(
        default=lambda s: fields.Date.today(),
        compute='_compute_request_date_onchange',
        store=True,
        readonly=False,
    )

    line_ids = fields.One2many(
        "library.checkout.line",
        "checkout_id",
        string="Borrowed Books",
    )
    stage_id = fields.Many2one(
        "library.checkout.stage",
        default=_default_stage_id,
        group_expand="_group_expand_stage_id")

    state = fields.Selection(related="stage_id.state")

    checkout_date = fields.Date(readonly=True)
    close_date = fields.Date(readonly=True)

    @api.model
    def create(self, vals):
        new_record = super().create(vals)
        if new_record.stage_id.state in ('open', 'close'):
            raise exceptions.UserError('State not allowed for new checkouts')
        return new_record

    def write(self, vals):
        if "stage_id" in vals and "kanban_state" not in vals:
            vals["kanban_state"] = "normal"
        old_state = self.stage_id.state
        super().write(vals)
        new_state = self.stage_id.state
        if not self.env.context.get('_checkout_write'):
            if new_state != old_state and new_state == 'open':
                self.with_context(
                    _checkout_write=True).write({'checkout_date': fields.Date.today()})
            if new_state != old_state and new_state == 'done':
                self.with_context(_checkout_write=True).write({'close_date': fields.Date.today()})
        return True

    def button_done(self):
        Stage = self.env["library.checkout.stage"]
        done_stage = Stage.search([("state", "=", "done")],
                                  limit=1)
        for checkout in self:
            checkout.stage_id = done_stage
        return True

    count_checkouts = fields.Integer(
        compute="_compute_count_checkouts"
    )
    num_books = fields.Integer(
        compute="_compute_num_books",
        store=True
    )

    kanban_state = fields.Selection(
        [("normal", "In Progress"),
         ("blocked", "Blocked"),
         ("done", "Ready for next stage")],
        "Kanban State",
        default="normal"
    )
    color = fields.Integer()

    priority = fields.Selection(
        [("0", "High"),
         "1", "Very High",
         ("2", "Critical")],
        default="0"
    )

    def _compute_count_checkouts(self):
        members = self.mapped("member_id")
        domain = [
            ("member_id", "in", members.ids),
            ("state", "not in", ["done", "cancel"])
        ]
        raw = self.read_group(domain, ["id:count"], ["member_id"])
        data = {
            x["member_id"][0]: x["member_id_count"] for x in raw
        }
        for checkout in self:
            checkout.count_checkouts = data.get(checkout.member_id.id, 0)

    @api.depends("line_ids")
    def _compute_num_books(self):
        for book in self:
            book.num_books = len(book.line_ids)
