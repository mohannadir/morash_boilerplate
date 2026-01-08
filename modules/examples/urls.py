from django.contrib import admin
from django.urls import path, include


from . import views

urlpatterns = [

    path('email/', views.EmailExample.as_view(), name='email'),

    path('credits/', views.CreditsExample.as_view(), name='credits'),
    path('credits/action/post/', views.CreditsActionExamplePOST.as_view(), name='credits_action_post'),
    path('credits/action/get/', views.CreditsActionExampleGET.as_view(), name='credits_action_get'),

    path('excel/', views.ExcelExample.as_view(), name='excel'),
    path('excel/export/', views.ExcelExportExample.as_view(), name='excel_export'),

    path('pdf/', views.PDFExample.as_view(), name='pdf'),
    path('pdf/export/', views.PDFExportExample.as_view(), name='pdf_export'),

    path('tables/', views.ExampleModelTable.as_view(), name='tables'),
    path('tables/data/', views.ExampleModelTableData.as_view(), name='tables_data'),

    path('websockets/', views.WebsocketsExample.as_view(), name='websockets'),

    path('file-generate/', views.LargeFileGenerateExample.as_view(), name='file_generate'),
    path('file-generate/start/', views.LargeFileGenerateStartTask.as_view(), name='file_generate_start_task'),

    path('form-wizard/', views.FormWizardExample.as_view(), name='form_wizard'),

    path('dall-e/', views.OpenAIDallEExample.as_view(), name='dall_e'),

]