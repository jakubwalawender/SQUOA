from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages


class SystemLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse(redirect('default'))

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
