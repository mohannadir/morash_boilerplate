from django.template.loader import render_to_string
from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

import datetime
import tablib

from modules.utils.pdf import render_to_pdf_file

class DynamicTableData(View):
    """ A view that returns the data for a dynamic table """

    template_name = None
    model = None
    context_object_name = 'objects'
    sort_default = 'pk'
    sort_options = []
    search_fields = []
    paginate_by = 10

    def get_search_term(self):
        """ Returns the search term from the request """
        return self.request.GET.get('search', None)
    
    def get_sort_field(self):
        """ Returns the field to sort by.
            
            If the sort parameter is in the request, it will be used.
            Otherwise, the first sort option will be used.
            If there are no sort options, the primary key will be used.
        """

        sort = self.request.GET.get('sort_field', None)
        if sort is not None:
            return sort
        
        return self.sort_default

    def get_per_page(self):
        """ Returns the number of items per page. 

            If the per_page parameter is in the request, it will be used.
            Otherwise, the paginate_by attribute will be used.
        """

        per_page = self.request.GET.get('per_page', None)
        if per_page is not None:
            return int(per_page)
        return self.paginate_by
    
    def get_template_name(self):
        """ Returns the template name to render the table """
        if self.template_name is not None:
            return self.template_name
        raise NotImplementedError('You must define a template_name or override the get_template_name method')
        
    def get_queryset(self):
        """" Returns the queryset to display in the table """
        if self.model is not None:
            return self.model.objects.all()
        raise NotImplementedError('You must define a model or override the get_queryset method')
    
    def get_processed_queryset(self):
        """ Returns the queryset after filtering, sorting and pagination. """
        sort_field = self.get_sort_field()
        queryset = self.get_queryset()
        search_term = self.get_search_term()
        
        search_query = None
        if search_term is not None and len(search_term) > 0 and len(self.search_fields) > 0:
            search_query = Q()
            for field in self.search_fields:
                search_query |= Q(**{f'{field}__icontains': search_term})

        if search_query is not None:
            queryset = queryset.filter(search_query)
        
        queryset = queryset.order_by(sort_field)

        page = self.request.GET.get('page', 1)
        per_page = self.get_per_page()
        paginator = Paginator(queryset, per_page)

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        
        return objects

    def get_html(self):
        """ Returns the html for the table """
        return render_to_string(self.get_template_name(), {self.context_object_name: self.get_processed_queryset()})
    
    def get(self, request, *args, **kwargs):
        """ Handles the GET request and returns the table data as JSON """
        objects = self.get_processed_queryset()

        return JsonResponse({
                'sort_default': self.sort_default,
                'sort_options': self.sort_options,
                'html': self.get_html(),
                'total': self.get_queryset().count(),
                'page': objects.number,
                'num_pages': objects.paginator.num_pages,
                'per_page': objects.paginator.per_page,
        })
    
class ExcelModelExport(View):
    """ A view that returns an Excel file with the data from a queryset """

    model = None
    fields = []
    filename = 'data.xlsx'

    def get_queryset(self):
        """ Returns the queryset to display in the table """
        if self.model is not None:
            return self.model.objects.all()
        raise NotImplementedError('You must define a model or override the get_queryset method')
    
    def get_fields(self):
        """ Returns the fields to display in the Excel file """
        if len(self.fields) > 0:
            return self.fields
        raise NotImplementedError('You must define fields or override the get_fields method')
    
    def format_field_value(self, value):
        """ Formats the value of a field """
        
        if isinstance(value, bool):
            return 'Yes' if value else 'No'
        elif value is None:
            return ''
        elif isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        
        return str(value)
    
    def get_formatted_fields(self):
        """ Formats fields to a dictionary, if necessary. """

        fields = self.get_fields()
        formatted_fields = []

        for field in fields:
            if isinstance(field, dict):
                if 'header' not in field or 'field' not in field:
                    raise ValueError('If you pass a field as a dictionary, it must have a header and a field key.')
                
                formatted_fields.append(field)
            elif isinstance(field, str):
                formatted_fields.append({'header': field, 'field': field})
        
        return formatted_fields
    
    def get_filename(self):
        """ Returns the filename of the Excel file """
        return self.filename
    
    def get(self, request, *args, **kwargs):
        """ Handles the GET request and returns the Excel file """

        queryset = self.get_queryset()
        fields = self.get_formatted_fields()
        data = tablib.Dataset()

        # Add headers
        data.append([field['header'] for field in fields])

        # Add data
        for objekt in queryset:
            data.append([self.format_field_value(getattr(objekt, field['field'])) for field in fields])

        response = HttpResponse(data.export('xlsx'), content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{self.get_filename()}"'
        return response
    
class PDFExport(View):
    """ A view that returns a PDF file """

    template_name = None
    filename = 'data.pdf'

    def get_template_name(self):
        """ Returns the template name to render the PDF """
        if self.template_name is not None:
            return self.template_name
        raise NotImplementedError('You must define a template_name or override the get_template_name method')
    
    def get_filename(self):
        """ Returns the filename of the PDF file """
        return self.filename
    
    def get_context(self, request, *args, **kwargs):
        """ Returns the context to render the PDF """
        return {}
    
    def get(self, request, *args, **kwargs):
        """ Handles the GET request and returns the PDF file """

        context = self.get_context(request, *args, **kwargs)
        pdf = render_to_pdf_file(self.get_template_name(), context)

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{self.get_filename()}"'
        return response