from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView, View
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.http import JsonResponse

from modules.emails.utils import send_email_from_base_template
from modules.billing.mixins import CreditActionMixin
from modules.views import ExcelModelExport, PDFExport, DynamicTableData
from modules.ai.openai import generate_image

from .seeder import ExampleSeeder
from .forms import SendTestEmailForm, ConsumeCreditForm, GenerateImageForm
from .models import ExampleModel
from .tasks import generate_large_file

## Example: Email
class EmailExample(LoginRequiredMixin, FormView):

    template_name = 'examples/email.html'
    form_class = SendTestEmailForm

    def form_valid(self, form):
        to_email = form.cleaned_data['to_email']
        send_email_from_base_template(
            to_emails=to_email,
            subject='Test Email',
            template_data = {
                'heading' : 'Test Email',
                'subheading' : 'This is a test email from ShipWithDjango',
                'content' : 'This is a test email from ShipWithDjango. If you received this email, it means that the email functionality is working correctly.',
                'buttons' : [
                    {
                        'text' : 'Go to Docs',
                        'url' : 'https://www.shipwithdjango.com',
                    }
                ]
            }
        )

        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, _('Test email sent successfully'))
        return reverse('examples:email')

## Example: Credits
class CreditsExample(LoginRequiredMixin, FormView):

    template_name = 'examples/credits.html'
    form_class = ConsumeCreditForm

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        action = form.cleaned_data['action']

        if self.request.user.has_credits(amount):
            self.request.user.consume_credits(amount, action)
            messages.success(self.request, _('Credits consumed successfully'))
        else:
            messages.error(self.request, _('You do not have enough credits to perform this action'))

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('examples:credits')
    
class CreditsActionExamplePOST(CreditActionMixin, TemplateView):
    amount_of_credits = 5
    action = 'You consumed 5 credits (POST action)'
    consume_credits_on = 'POST'

    template_name = 'examples/credits_action.html'

    def get_failed_url(self):
        messages.error(self.request, _('You do not have enough credits to perform this action'))
        return reverse('examples:credits')
    
    def get_success_url(self):
        messages.success(self.request, _('Credits consumed successfully'))
        return reverse('examples:credits')
    
class CreditsActionExampleGET(CreditActionMixin, View):
    amount_of_credits = 5
    action = 'You consumed 5 credits (GET action)'
    consume_credits_on = 'GET'

    def get_failed_url(self):
        messages.error(self.request, _('You do not have enough credits to perform this action'))
        return reverse('examples:credits')

    def get_success_url(self):
        messages.success(self.request, _('Credits consumed successfully'))
        return reverse('examples:credits')

## Example: Excel export
class ExcelExample(LoginRequiredMixin, TemplateView):
    template_name = 'examples/excel.html'

class ExcelExportExample(ExcelModelExport):
    model = get_user_model()

    # You can pass fields as a list of strings or a list of dictionaries
    # If you pass a list of strings, the header will be the field name
    # If you pass a list of dictionaries, you can specify the header and the field name

    # fields = ['id', 'username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined', 'is_active']
    fields = [
        {'header' : 'id', 'field': 'id' },
        {'header' : 'Username', 'field': 'username' },
        {'header' : 'First Name', 'field': 'first_name' },
        {'header' : 'Last Name', 'field': 'last_name' },
        {'header' : 'Email', 'field': 'email' },
        {'header' : 'Last Login', 'field': 'last_login' },
        {'header' : 'Date Joined', 'field': 'date_joined' },
        {'header' : 'Is Active', 'field': 'is_active' },
    ]

## Example: PDF export
class PDFExample(LoginRequiredMixin, TemplateView):
    template_name = 'examples/pdf.html'

class PDFExportExample(PDFExport):
    template_name = 'examples/pdf_file_template.html'
    
    def get_context(self, request, *args, **kwargs):
        return {
            'current_user' : request.user,
            'generated_at' : timezone.now(),
            'heading' : 'PDF Export Example',
            'subheading' : 'This is a PDF export example from ShipWithDjango',
            'content' : 'This is a PDF export example from ShipWithDjango. If you downloaded this PDF, it means that the PDF export functionality is working correctly.',
        }

## Example: Table with server-side processing
class ExampleModelTable(LoginRequiredMixin, TemplateView):
    template_name = 'examples/tables/tables.html'

    def post(self, request, *args, **kwargs):
        seeder = ExampleSeeder(count=200)
        seeder.clear()
        seeder.run()
        messages.success(request, _('Example data seeded successfully'))
        return super().get(request, *args, **kwargs)

class ExampleModelTableData(LoginRequiredMixin, DynamicTableData):
    template_name = 'examples/tables/data.html'
    model = ExampleModel
    context_object_name = 'example_models'
    sort_options = [{ 'name': 'Name', 'field': 'name', }, { 'name': 'Address', 'field': 'address', }]
    sort_default = 'name'
    search_fields = ['name', 'address']

    def get_queryset(self):
        return ExampleModel.objects.all()
    
## Example: Xebsockets
class WebsocketsExample(LoginRequiredMixin, TemplateView):
    template_name = 'examples/websockets.html'

## Example: File generation with tasks
class LargeFileGenerateExample(LoginRequiredMixin, TemplateView):
    template_name = 'examples/large_file_generate.html'

class LargeFileGenerateStartTask(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        task = generate_large_file()
        return JsonResponse({'task_id': task.id})

## Example: Form wizard
class FormWizardExample(LoginRequiredMixin, TemplateView):
    template_name = 'examples/form_wizard.html'

## Example: OpenAI Dall-E
class OpenAIDallEExample(LoginRequiredMixin, FormView):
    template_name = 'examples/openai_dalle.html'
    form_class = GenerateImageForm

    def form_valid(self, form):
        prompt = form.cleaned_data['prompt']
        size = form.cleaned_data['size']
        quality = form.cleaned_data['quality']
        image = generate_image(prompt, size, quality)
        return JsonResponse({'base64_image': image})