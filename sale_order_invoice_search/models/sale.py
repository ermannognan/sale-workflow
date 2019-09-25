# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import api, fields, _
from odoo.osv import osv


class SaleOrder(osv.Model):
    _inherit = 'sale.order'

    invoice_ids = fields.Many2many(
        "account.invoice", compute="_get_invoiced",
        copy=False, search='_search_orders_by_invoice_ids')

    def _search_orders_by_invoice_ids(self, operator, value):
        if operator in ('like', 'ilike'):
            value = self.env['account.invoice'].search([
                ('number', operator, value),
            ]).ids
            operator = 'in'
        assert operator in ('=', 'in'), \
            _('Operator %s not supported, use "in"') % operator
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
