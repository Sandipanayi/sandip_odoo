# -*- coding:utf-8 -*-
from odoo import models,fields,api,_
from odoo.exceptions import ValidationError,UserError


class Carrier(models.Model):
    _name='carrier.carrier'

    name=fields.Char(size=128,required=True,string='Name')
    product_category_id=fields.Many2one('product.category')
    from_location_id=fields.Many2one('routing.location',required=True)
    to_location_id=fields.Many2one('routing.location',required=True)
    provider_lines_ids=fields.One2many('carrier.provider','carrier_id')

    @api.constrains('from_location_id','to_location_id')
    def _check_code(self):
        for record in self:
            if record.from_location_id==record.to_location_id:
                raise ValidationError("Your root is invalid")

