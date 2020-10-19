# -*- coding:utf-8 -*-
from odoo import models,fields,api,_
from odoo.exceptions import ValidationError,UserError


class Carrier_lines(models.Model):
	_name='carrier.lines'

	provider_id=fields.Many2one('carrier.provider')
	from_location_id=fields.Many2one('routing.location')
	to_location_id=fields.Many2one('routing.location')
	medium=fields.Selection([('by sea','By sea'),('by air','By Air'),('by bus','By Bus'),('by train','By train')])
	distance=fields.Float()
	days=fields.Float()
	price=fields.Float()
	weight=fields.Float()

	@api.constrains('from_location_id','to_location_id')
	def _check_code(self):
		for record in self:
			if record.from_location_id == record.to_location_id:
				raise ValidationError("Your root is invalid")

