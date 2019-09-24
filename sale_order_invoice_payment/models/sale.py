# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import api, fields
from odoo.osv import osv

PAYMENT_STATES = [
    ('waiting', 'Waiting for payments'),
    ('done', 'Paid'),
    ('no', 'Not to pay')
]


class SaleOrder(osv.Model):
    _inherit = 'sale.order'

    payment_status = fields.Selection(
        string="Payment status", selection=PAYMENT_STATES,
        compute='_get_payment_info', store=True)
    invoice_ids = fields.Many2many(
        "account.invoice", compute="_get_invoiced",
        copy=False, search='_search_orders_by_invoice_ids')

    def _search_orders_by_invoice_ids(self, operator, value):
        assert operator in ('=', 'in'), \
            _('Operator %s not supported, use "ilike"') % operator
        if isinstance(value, (int, long)):
            value = [value]
        self.env.cr.execute("""
            SELECT DISTINCT so.id 
            FROM sale_order_line_invoice_rel AS rel
            INNER JOIN account_invoice_line AS invl
                ON invl.id = rel.invoice_line_id
            INNER JOIN account_invoice AS inv
                ON inv.id = invl.invoice_id
            INNER JOIN sale_order_line AS sol
                ON sol.id = rel.order_line_id
            INNER JOIN sale_order AS so
                ON so.id = sol.order_id
            WHERE inv.id IN %s AND 
                inv.type IN ('out_invoice', 'out_refund')
        """, (tuple(value),))
        ids = [r[0] for r in self.env.cr.fetchall()]
        return [('id', 'in', ids)]

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
