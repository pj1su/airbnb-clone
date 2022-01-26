from django.views import View
from django.shortcuts import render
from . import forms

# form_vaild는 HttpResponse형태이기떄문에 redirect-> reverse해야함
class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={"email": "wltn@qkr.com"})  # 미리 입력되어있게
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        return render(request, "users/login.html", {"form": form})
