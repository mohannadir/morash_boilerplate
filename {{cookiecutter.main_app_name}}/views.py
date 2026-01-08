from typing import Any
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class LandingPage(TemplateView):
    """ A view that renders the landing page """

    template_name = '{{ cookiecutter.main_app_name }}/landing.html'

class Dashboard(LoginRequiredMixin, TemplateView):
    """ A view that renders the dashboard """
    template_name = '{{ cookiecutter.main_app_name }}/dashboard.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(**kwargs)