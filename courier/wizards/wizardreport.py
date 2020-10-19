# -*- coding:utf-8 -*-

from odoo import models,fields,api,_


class WizardReport(models.TransientModel):
    _name = 'wizardr.wizardr'

    sdate = fields.Date(string="Start-Date",required=True)
    edate = fields.Date(string="End-Date",required=True)
    routing_id = fields.Many2one('routing.routing',required=True,string="Routing")
    carrier_id = fields.Many2one('carrier.carrier',string="Carrier",required=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('return','Return'),
        ('cancel','Cancel'),
        ('done','Done'),
        ('cancel','Cancel'),
        ('done','Done')],required=True,default='draft')

    @api.multi
    def Print_Report(self):
        return self.env.ref('courier.wizard_report_id').report_action(self)






