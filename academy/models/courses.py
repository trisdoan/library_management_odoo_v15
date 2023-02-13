from odoo import models, fields


class Courses(models.Model):
    _name = 'academy.courses'
    _inherit = 'mail.thread'
    name = fields.Char()
    teacher_id = fields.Many2one('academy.teachers', string="Teacher")
