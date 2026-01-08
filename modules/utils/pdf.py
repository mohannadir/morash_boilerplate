import weasyprint
from django.template.loader import render_to_string

def render_to_pdf_file(template_src: str, context_dict: dict) -> bytes:
    """ Render a Django template to a PDF file. """
    
    html_string = render_to_string(template_src, context_dict)
    html = weasyprint.HTML(string=html_string)
    result = html.write_pdf()
    return result