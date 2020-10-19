# -*- coding:utf-8 -*-

from odoo import models,fields,api,_

class WizardNew(models.TransientModel):
    _name="changev.changev"

    courier_from_id = fields.Many2one('res.partner',required=True)
    courier_to_id = fields.Many2one('res.partner',required=True)

    @api.multi
    def change_location(self,values):
        res = self.env['courier.courier'].search([])
        vals = {
            'courier_from_id':self.courier_from_id.id,
            'courier_to_id':self.courier_to_id.id,
        }
        res.write(vals)

