# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Teacher(models.Model):
    _name = 'academy.teachers'
    name = fields.Char()
    biography = fields.Html()
    course_ids = fields.One2many("academy.courses", "teacher_id", string="Courses")
