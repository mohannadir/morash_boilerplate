from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, FileResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
import os

from huey.contrib.djhuey import HUEY

class HueyCheckFileTaskStatus(LoginRequiredMixin, View):
    """ View to check the status of a file task. 
        If the task is completed, the file will be downloaded.

        NOTE: This only works if Huey is configured to store the results and the result of the task is the file path to download.
    """

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id', None)
        if not task_id:
            return HttpResponseBadRequest()
        
        try:
            file_path = HUEY.result(task_id)
        except Exception as e:
            return JsonResponse({'state': 'ERROR', 'error': str(e)}, status=500)
        
        if file_path:
            if default_storage.exists(file_path):
                response = FileResponse(default_storage.open(file_path, 'rb'))
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
                
                # The data has already been placed in the response, so we can delete the file
                default_storage.delete(file_path)
                
                return response
            else:
                return HttpResponseNotFound('File not found')
        else:
            return JsonResponse({'state': 'PENDING'}, status=202)