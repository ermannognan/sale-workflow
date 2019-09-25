# -*- coding: utf-8 -*-

{
    'name': 'Sale Order Invoice Payment',
    'version': '1.0',
    'category': 'Sale Extensions',
    'description': """
Tech Plus Sale.
""",
    'author': 'Ermanno Gnan',
    'website': '',
    'summary': """
        This module adds the payment state adding a new field on sale orders.
        A sale order is considered paid if it is fully invoiced and all invoiced
        are paid.
        """,
    'sequence': 1,
    'depends': [
        'sale_order_invoice_search',
    ],
    'data': [
        'views/sale_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': True,
}
