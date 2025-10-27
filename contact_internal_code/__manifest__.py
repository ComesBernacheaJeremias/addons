{
    'name': 'Internal Code for Contacts',
    'version': '18.0.1.0.0',
    'category': 'Contacts',
    'summary': 'Add internal code field to contacts',
    'description': """
        This module adds an internal code field to the contact form.
    """,
    'author': 'Tu Nombre',
    'website': 'https://tusitio.com',
    'depends': ['base', 'contacts'],
    'data': [
        'views/contact_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}