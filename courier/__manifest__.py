# -*- coding: utf-8 -*-
# Part of Synconics. See LICENSE file for full copyright and licensing details.

{
    'name': 'courier',
    'version': '12.0',
    'summary': """

    """,
    'sequence': 1,
    'description': """

    """,
    'category': "courier",
    'author': 'Synconics Technologies Pvt. Ltd.',
    'website': 'http://www.synconics.com',
    'depends': ['base','mail','stock','account'],
    'data': [
            'data/seq.xml',
            # 'data/data.xml',
            'views/courier_exel_report.xml',
            'views/courier_report.xml',
            'views/customer.xml',
            'security/ir.model.access.csv',
            'views/courier.xml',
            'views/routing_location.xml',
            'views/carrier.xml',
            'views/provider_lines.xml',
            'views/carrier_lines.xml',
            'views/routing.xml',
            'views/product.xml',
            'views/newproduct.xml',
            'data/mailnew.xml',
            'wizards/changelocation.xml',
            'wizards/wizardreport.xml',
            'wizards/wizard_report.xml',
            'views/courier_report_pivot.xml',
            'views/pivot_courier_report.xml',

    ],
    'demo': [],

    'images': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}