from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView
from django.db.models import Count, F, Case, When, CharField, Value
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from cinema.models import UserMovieList
from orders.models import Order
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


class AccountView(TemplateView):
    template_name = 'user/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        movie_stats = UserMovieList.objects.filter(user=user).values(
            'list_type'
        ).annotate(
            count=Count('id'),
            list_name=Case(
                *[
                    When(list_type=list_type, then=Value(value))
                    for list_type, value in UserMovieList.LIST_TYPES
                ],
                output_field=CharField()
            )
        ).order_by('list_type')

        context['movie_stats'] = movie_stats
        context['recent_orders'] = Order.objects.filter(user=user).order_by('-created')[:3]
        context['recent_movies'] = UserMovieList.objects.filter(
            user=user
        ).select_related('movie').order_by('-added_at')[:4]

        return context
