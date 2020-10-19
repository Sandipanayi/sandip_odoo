# -*- coding:utf-8 -*-

from odoo import models,fields,api,_
from datetime import date
from odoo.exceptions import ValidationError,UserError


class Courier(models.Model):
    _name='courier.courier'
    _inherit='mail.thread'
    _description = 'courier'

    name = fields.Char(string='Name',size=128,required=True)
    confirmed_date = fields.Date(string='Date',readonly=True)
    courier_from_id = fields.Many2one('res.partner',required=True)
    courier_to_id = fields.Many2one('res.partner',required=True)
    routing_id = fields.Many2one('routing.routing',required=True)
    invoice_id = fields.Many2one('account.invoice')
    delivery_id = fields.Many2one('stock.picking')
    delivery_date = fields.Date(readonly=True)
    total_price = fields.Float(string="Total Price",compute="_compute_again_total",store=True)
    real_delivery_date = fields.Date(string='Real delivery date')
    notes = fields.Text()
    invoice_count = fields.Integer(compute="_compute_invoice")
    get_invoice = fields.Many2many('account.invoice',string="get_invoice")
    delivery_count = fields.Integer(compute="_compute_del")
    get_delivery = fields.Many2many('stock.picking',string="get_delivery")
    carrier_id = fields.Many2one('carrier.carrier')
    user_id = fields.Many2one('res.users',default=lambda self: self.env.user.id)
    carrier_lines_ids = fields.One2many('carrier.provider','carrier_id',compute="get_values")
    courier_product_line_ids = fields.One2many('courier.product.lines','courier_id')
    nameseq = fields.Char(string='Order no', required=True, copy=False, readonly=True,
                          index=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('return','Return'),
        ('cancel','Cancel'),
        ('done','Done'),
        ('invoice','Invoice'),
        ('delivery','Delivery'),
        ('reset to darft','Reset to darft')],required=True,default='draft')

    @api.multi
    def button_draft(self):
        for rec in self:
            rec.write({'state':'draft'})

    @api.multi
    def button_done(self):
        for rec in self:
            rec.write({'state':'done'})

    @api.multi
    def button_confirm(self):
        for rec in self:
            rec.write({'state':'confirm'})

    @api.multi
    def button_delivery(self):
        for rec in self:
            rec.write({'state':'delivery'})

    @api.multi
    def button_cancel(self):
        for rec in self:
            rec.write({'state':'cancel'})

    @api.multi
    def button_return(self):
        for rec in self:
            rec.write({'state':'return'})

    @api.multi
    def button_invoice(self):
        for rec in self:
            rec.write({'state':'invoice'})

    @api.multi
    def button_resettodraft(self):
        for rec in self:
            rec.state='draft'

    @api.model
    def create(self, vals):
        if vals.get('nameseq', _('New')) == _('New'):
            vals['nameseq'] = self.env['ir.sequence'].next_by_code('courier.courier.new') or _('New')
            result = super(Courier, self).create(vals)
            return result

    @api.constrains('courier_product_line_ids')
    def button_confirm(self):
        for record in self:
            if record.courier_product_line_ids:
                record.write({'state':'confirm'})
            else:
                raise ValidationError("Please select Your product")

    @api.onchange('routing_id')
    @api.constrains('courier_product_line_ids')
    def get_values(self):
        for data in self:
            if data.courier_product_line_ids:
                if data.routing_id:
                    providers = data.routing_id.provider_lines_ids.filtered(lambda r: r.selected)
                    data.carrier_lines_ids = [(6, 0 , providers.ids)]
                else:
                    raise ValidationError("Please select Your product")

    @api.depends('courier_product_line_ids','carrier_lines_ids','routing_id')
    def _compute_again_total(self):
        for rec in self:
            rec.new_weight = sum(rec.courier_product_line_ids.mapped('total_weight'))
            other_weight = rec.carrier_lines_ids.weight
            if rec.new_weight > other_weight:
                rec.total_price = rec.carrier_lines_ids.price + rec.carrier_lines_ids.extra_price
            else:
                rec.total_price = rec.carrier_lines_ids.price

    @api.constrains('courier_from_id','courier_to_id')
    def _check_code(self):
        for record in self:
            if record.courier_from_id == record.courier_to_id:
                raise ValidationError("Your Courier Path is invalid")

    @api.multi
    def button_printreport(self):
        return self.env.ref('courier.courier_report_id').report_action(self)

    @api.multi
    def button_sendemail(self):
        self.ensure_one()
        template = self.env.ref('courier.new_mail_email_id')
        compose_form = self.env.ref('mail.email_compose_message_wizard_form')
        ctx = dict(
            default_model='courier.courier',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            custom_layout="mail.mail_notification_light",
            )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    @api.multi
    def search_invoice(self):
        action = {
            'name': _('Invoices'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'account.invoice',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', [x.id for x in self.get_invoice])],
        }
        action['views'] = [(self.env.ref('account.invoice_tree').id, 'tree'), (self.env.ref('account.invoice_form').id, 'form')]
        return action

    @api.multi
    def _compute_invoice(self):
        for rec in self:
            rec.invoice_count = len(rec.get_invoice)

    def button_invoice(self):
        for rec in self:
            invoice = self.env['account.invoice'].create(
                {
                'partner_id': rec.courier_to_id.id,
                'invoice_id': self.get_invoice,
            })
            account = self.env.user.company_id.get_chart_of_accounts_or_fail()
            for product_line in self.courier_product_line_ids:
                self.env['account.invoice.line'].create({
                    'quantity': 1,
                    'price_unit':self.total_price,
                    'invoice_id': invoice.id,
                    'name': self.name,
                    'account_id': account.id,

                })
                self.get_invoice = [(4, invoice.id)]

    @api.multi
    def _compute_del(self):
        for rec in self:
            rec.delivery_count = len(rec.get_delivery)

    def button_delivery(self):
        for rec in self:
            rec.delivery_date = fields.Date.today()
            # rec.real_delivery_date = fields.Date.today()
            delivery = self.env['stock.picking'].create(
                {
                'partner_id':self.courier_from_id.id,
                'delivery_id': self.get_delivery,
                'location_id': self.courier_from_id.id,
                'location_dest_id': self.courier_to_id.id,
                'picking_type_id': self.routing_id.id,
            })
            for products_line in self.courier_product_line_ids:
                self.env['stock.move'].create({
                    'location_id': self.courier_from_id.id,
                    'location_dest_id': self.courier_to_id.id,
                    'name':'mj',
                    'product_id': products_line.product_id.id,
                    'product_uom': 1,
                    'product_uom_qty': products_line.qty,
                    'picking_id': delivery.id,
                    'quantity_done': products_line.total_weight,
            })
            self.get_delivery = [(4, delivery.id)]

    def action_view_mo_delivery(self):
        self.ensure_one()
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        pickings = self.mapped('get_delivery')
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        return action





# class AccountPayment(models.Model):
#     _inherit = "account.invoice"

#     state = fields.Selection([
#             ('draft','Draft'),
#             ('open', 'Open'),
#             ('in_payment', 'In Payment'),
#             ('paid', 'Paid'),
#             ('cancel', 'Cancelled'),
#         ], string='Status', index=True, readonly=True, default='draft',
#         track_visibility='onchange',copy=False,
#         help=" * The 'Draft' status is used when a user is encoding a new and unconfirmed Invoice.\n"
#              " * The 'Open' status is used when user creates invoice, an invoice number is generated. It stays in the open status till the user pays the invoice.\n"
#              " * The 'In Payment' status is used when payments have been registered for the entirety of the invoice in a journal configured to post entries at bank reconciliation only, and some of them haven't been reconciled with a bank statement line yet.\n"
#              " * The 'Paid' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled.\n"
#              " * The 'Cancelled' status is used when user cancel invoice.")






# class StudentDatas(models.Model):
#     _inherit="account.invoice"

#     def paid_button(self):
#         for rec in self:
#             if rec.state:
#                 if rec.state == 'paid':
#                     rec.button_delivery()


    # state = fields.Selection([
    #         ('draft','Draft'),
    #         ('open', 'Open'),
    #         ('in_payment', 'In Payment'),
    #         ('paid', 'Paid'),
    #         ('cancel', 'Cancelled'),
    #     ], string='Status', index=True, readonly=True, default='draft',
    #     track_visibility='onchange', copy=False,
    #     help=" * The 'Draft' status is used when a user is encoding a new and unconfirmed Invoice.\n"
    #          " * The 'Open' status is used when user creates invoice, an invoice number is generated. It stays in the open status till the user pays the invoice.\n"
    #          " * The 'In Payment' status is used when payments have been registered for the entirety of the invoice in a journal configured to post entries at bank reconciliation only, and some of them haven't been reconciled with a bank statement line yet.\n"
    #          " * The 'Paid' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled.\n"
    #          " * The 'Cancelled' status is used when user cancel invoice.")

#     @api.multi
#     def cancel(self):
#         for rec in self:
#             if rec.get_invoice!='paid':
#                 invisible.button_delivery()


    # @api.multi
    # def _write(self, vals):
    #     res = super(Courier, self)._write(vals)
    #     if vals.get('paid'):
    #      # if there is any search filters you can give it
    #         pos_admin_rec = self.env['account.invoice'].search([])
    #         if rec.state == 'paid':
    #             rec.button_delivery()
    #         else:
    #             ValidationError("sorry")
    #          #here call the function in pos.admin model
    #              pos_rec._write()
    #     return res

