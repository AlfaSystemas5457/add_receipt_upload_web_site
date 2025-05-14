{
    'name': 'Subir recibos desde el website',
    'version': '1.0',
    'description': 'Extension para subir recibos de pago',
    'summary': 'Extension para subir recibos de pago',
    'author': 'DGV',
    # 'website': '',
    'license': 'LGPL-3',
    'category': 'Other category',
    'depends': [
        'website_sale',
        'mail',
    ],
    'data': [
        'data/email_template_view.xml',
        'views/website_templates.xml',
        'views/custom_payment_receipt_upload_view.xml',
    ],
    'auto_install': False,
    'application': False,
    'sequence': 0,
}
