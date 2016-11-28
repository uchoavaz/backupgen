
# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import auth
from django.shortcuts import redirect
from apps.accounts.models import BackupUser
from django.contrib import messages
from django.utils import timezone
from apps.accounts.forms import PasswordForm


def login(request):
    template_name = 'login.html'
    context = {}

    email = request.POST.get('email')
    password = request.POST.get('password')

    context['email_label'] = BackupUser._meta.get_field(
        "email").verbose_name.title()
    context['password_label'] = BackupUser._meta.get_field(
        "password").verbose_name.title()

    if email and password:
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                user.last_access = timezone.now()
                user.save()
                return redirect(reverse_lazy('core:home'))
            else:
                messages.error(request, u'Usuário não está ativo')
        else:
            messages.error(request, u'Usuário ou senha não existente')
    return render(request, template_name, context)


def logout(request):
    request.user.last_access = timezone.now()
    request.user.save()
    auth.logout(request)
    return redirect(reverse_lazy('accounts:login'))


class PasswordView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy("accounts:login")
    template_name = 'password.html'
    form_class = PasswordForm
    success_url = reverse_lazy('core:home')

    def get_form(self, form_class):
        user = BackupUser.objects.get(email=self.request.user.email)
        return form_class(instance=user, **self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(
            self.request,
            'Sua senha foi alterada! Entre no sistema com sua nova senha')
        return redirect(reverse_lazy('accounts:logout'))

password = PasswordView.as_view()
