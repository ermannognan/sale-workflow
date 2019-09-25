# -*- coding: utf-8 -*-

{
    'name': 'Sale Order Invoice Search',
    'version': '1.0',
    'category': 'Sale Extensions',
    'description': """
Tech Plus Sale.
""",
    'author': 'Ermanno Gnan',
    'website': '',
    'summary': """
        This module adds the sale order search by invoice.
        """,
    'sequence': 1,
    'depends': [
        'sale',
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
