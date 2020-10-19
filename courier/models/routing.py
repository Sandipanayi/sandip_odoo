# -*- coding:utf-8 -*-
from odoo import models,fields,api,_
from odoo.exceptions import ValidationError,UserError


class Carrier(models.Model):
    _name='routing.routing'

    name=fields.Char()
    from_location_id=fields.Many2one('routing.location',required=True)
    to_location_id=fields.Many2one('routing.location',required=True)
    distance=fields.Float()
    days=fields.Float()
    price=fields.Float()
    path_id=fields.Many2one('carrier.carrier')
    provider_lines_ids=fields.One2many('carrier.provider','provider_id',related="path_id.provider_lines_ids")

    @api.constrains('from_location_id','to_location_id')
    def _check_code(self):
        for record in self:
            if record.from_location_id==record.to_location_id:
                raise ValidationError("Your root is invalid")


    # @api.multi
    # def name_get(self):
    #   res=[]
    #   for fields in self:
    #       res.append((fields.id,"%s,%d"%(fields.name,fields.days)))
    #       return res


