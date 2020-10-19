# -*- coding:utf-8 -*-

from odoo import models, fields, api, _


class Productnew(models.Model):
    _name = 'courier.product.lines'

    product_id = fields.Many2one('product.product',string="Product",required=True)
    qty = fields.Float(string="Quantity")
    courier_id = fields.Many2one('courier.courier')
    total_weight = fields.Float(string="Total Weight",compute="_total_all_weight")

    @api.multi
    @api.depends('product_id', 'qty')
    def _total_all_weight(self):
        for rec in self:
            total_weight = 0.0
            if rec.product_id and rec.product_id.weight:
                total_weight = rec.product_id.weight * rec.qty
            rec.total_weight = total_weight


