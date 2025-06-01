from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import redirect
from django.views.generic import FormView

from .forms import RegisterForm, LoginForm


class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = 'user/login.html'


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'user/register.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())
