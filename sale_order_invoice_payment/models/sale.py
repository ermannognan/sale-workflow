# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import api, fields
from odoo.osv import osv

PAYMENT_STATES = [
    ('waiting', 'Waiting for payment'),
    ('done', 'Paid'),
    ('no', 'Not to pay')
]


class SaleOrder(osv.Model):
    _inherit = 'sale.order'

    payment_status = fields.Selection(
        string="Payment status", selection=PAYMENT_STATES,
        compute='_get_payment_info', store=True)

    @api.multi
    @api.depends('invoice_status', 'invoice_ids.state')
    def _get_payment_info(self):
        for order in self:
            status = 'no'
            if order.invoice_status != 'no':
                if order.invoice_status == 'invoiced' and \
                        not order.invoice_ids.filtered(
                            lambda i: i.state not in ('paid', 'cancel')):
                    status = 'done'
                else:
                    status = 'waiting'
            order.payment_status = status
