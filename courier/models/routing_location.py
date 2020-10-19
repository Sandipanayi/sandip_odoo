# -*- coding:utf-8 -*-

from odoo import models, fields, api, _


class RoutingLocation(models.Model):
    _name='routing.location'

    name=fields.Char(size=128,required=True)
    code=fields.Char(size=4,required=True)
    sequence = fields.Integer('sequence')

    # _sql_constraints = [('course_unique', 'unique(code)', 'Code should be unique')]
