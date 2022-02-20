from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:home")


class LoggedOutOnlyView(UserPassesTestMixin):  # UserPassesTestMixin사용자가 정의

    permission_denied_message = "Page not found"

    def test_func(self):  # Ture반환하면 허용
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:home")


# @login_required 과 같다
class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")
