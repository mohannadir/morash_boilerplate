from django.utils.translation import gettext_lazy as _

EXAMPLES_SUBNAV = {
    'key' : 'examples',
    'name' : _('Examples'),
    'show_title' : True,
    'is_active' : True,
    'items' : [{
        'key': 'example_email',
        'name': _('Email'),
        'url_name' : 'examples:email',
        'icon': 'mail',
        'is_active': True,
    },
    {
        'key': 'example_credits',
        'name': _('Credits'),
        'url_name' : 'examples:credits',
        'icon': 'box',
        'is_active': True,
    },
    {
        'key': 'example_excel',
        'name': _('Excel export'),
        'url_name' : 'examples:excel',
        'icon': 'file',
        'is_active': True,
    },
    {
        'key': 'example_pdf',
        'name': _('PDF export'),
        'url_name' : 'examples:pdf',
        'icon': 'file-text',
        'is_active': True,
    },
    {
        'key': 'example_tables',
        'name': _('Dynamic tables'),
        'url_name' : 'examples:tables',
        'icon': 'table',
        'is_active': True,
    },
    {
        'key': 'example_websockets',
        'name': _('Websockets'),
        'url_name' : 'examples:websockets',
        'icon': 'message-square',
        'is_active': True,
    },
    {
        'key': 'example_large_files',
        'name': _('Generate large files'),
        'url_name' : 'examples:file_generate',
        'icon': 'download',
        'is_active': True,
    },
    {
        'key': 'example_form_wizard',
        'name': _('Form wizard'),
        'url_name' : 'examples:form_wizard',
        'icon': 'layers',
        'is_active': True,
    },
    {
        'key': 'example_dalle',
        'name': _('Images with Dall-E'),
        'url_name' : 'examples:dall_e',
        'icon': 'image',
        'is_active': True,
    }
    ]
}