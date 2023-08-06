import os
import os.path
from nbconvert.nbconvertapp import NbConvertApp
from nbconvert.exporters.html import HTMLExporter
from nbconvert.exporters.pdf import PDFExporter
from .utils import ENV_VARS


_html_no_code_template = os.environ.get(ENV_VARS['export_html'], '') or os.path.join(os.path.dirname(__file__), 'templates', 'hide_code_cells_html.tpl')
_pdf_no_code_template = os.environ.get(ENV_VARS['export_pdf'], '') or os.path.join(os.path.dirname(__file__), 'templates', 'hide_code_cells_pdf.tplx')
_html_no_code_email_template = os.environ.get(ENV_VARS['export_html_email'], '') or os.path.join(os.path.dirname(__file__), 'templates', 'hide_code_cells_html_email.tpl')


def export_pdf(nbpath, template=_pdf_no_code_template):
    NbConvertApp.launch_instance([nbpath, '--template', template, '--to', 'pdf'])


def export_html(nbpath, template=_html_no_code_template):
    NbConvertApp.launch_instance([nbpath, '--template', template, '--to', 'html'])


class HTMLHideCodeExporter(HTMLExporter):
    export_from_notebook = "HTML - No Code"

    # exclude_input = True
    def _file_extension_default(self):
        return '.html'

    @property
    def template_path(self):
        if os.environ.get(ENV_VARS['export_html'], ''):
            return super(HTMLHideCodeExporter, self).template_path + [os.path.dirname(os.environ.get(ENV_VARS['export_html']))]
        return super(HTMLHideCodeExporter, self).template_path + [os.path.join(os.path.dirname(__file__), 'templates')]

    def _template_file_default(self):
        return 'hide_code_cells_html.tpl'


class PDFHideCodeExporter(PDFExporter):
    export_from_notebook = "PDF - No Code"


    def _file_extension_default(self):
        return '.pdf'

    @property
    def template_path(self):
        if os.environ.get(ENV_VARS['export_pdf'], ''):
            return super(PDFHideCodeExporter, self).template_path + [os.path.dirname(os.environ.get(ENV_VARS['export_pdf']))]
        return super(PDFHideCodeExporter, self).template_path + [os.path.join(os.path.dirname(__file__), 'templates')]

    def _template_file_default(self):
        return 'hide_code_cells_pdf.tplx'
