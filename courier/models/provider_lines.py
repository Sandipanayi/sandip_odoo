# -*- coding:utf-8 -*-
from odoo import models,fields,api,_


class ProviderLines(models.Model):
	_name='carrier.provider'

	carrier_id = fields.Many2one('carrier.carrier',required=True)
	provider_id = fields.Many2one('res.partner',required=True)
	distnace = fields.Float()
	days = fields.Float()
	price = fields.Float()
	weight = fields.Float()
	extra_price = fields.Float()
	selected = fields.Boolean()
	carrier_lines_ids = fields.One2many('carrier.lines','provider_id')


