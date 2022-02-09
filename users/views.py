from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import models

# authenticate는 username이 필요하기때문에 username을 email이랑 같이 관리자패널에서 바꾸고 로그인
from . import forms

# username으로 인증이 괜찮으면 LoginView클래스 상속(더 간단하긴함)
# form_vaild는 HttpResponse형태이기떄문에 redirect-> reverse해야함

# class LoginView(View):
#     def get(self, request):
#         form = forms.LoginForm(initial={"email": "wltn5055@naver.com"})  # 미리 입력되어있게
#         return render(request, "users/login.html", {"form": form})

# def post(self, request):
#     form = forms.LoginForm(request.POST)
#     if form.is_valid():
#         email = form.cleaned_data.get("email")
#         password = form.cleaned_data.get("password")
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect(reverse("core:home"))
#     # print(form.is_valid())
#     return render(request, "users/login.html", {"form": form})


# def log_out(request):  # class LoginView도 있음 document
#     logout(request)
#     return redirect(reverse("core:home"))

# LoginView 말고 FormView사용 권장 username을 쓰게함
class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    initial = {"email": "wltn5055@naver.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):  # class LogouView도 있음 document
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "jisu",
        "last_name": "pakr",
        "email": "wltn5055@naver.com",
    }

    def form_valid(self, form):  # form에 user을 저장x
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"  # 이걸 지정안하면 룸 디테일에 룸호스트를 누르면 그룸의 사용자로 로그인된다 유저디테일 템플릿에서 user. 으로하면 모든 룸의 유저든 모두 바뀔 수 있으니 context지정후 써야함


# 이걸 지정할땐 유저모델에 앱솔루트 지정해서 pk인자값 받아오게

# url에서 pk를 받지 않기떄문에 get object를 써서 우리가 수정하기를 원하는 객체를 반환
class UpdateUserView(UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        # "email",
        # "username",  username을 밑에 폼 벨리드로 인터셉트가능 이메일이랑 유저네임 같게 하고싶은데 유저들한테 안보이게 할려면
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )

    def get_object(
        self, queryset=None
    ):  # 수정하고싶은 객체 반환 self , url에 int:pk가 없지만 유저를 줄때 ex) "update/"
        return self.request.user

    # def form_valid(self, form):
    #     email = form.cleaned_data.get("email")
    #     self.object.username = email
    #     self.object.save()
    #     return super().form_valid(form)


class UpdatePasswordView(PasswordChangeView):
    # pass 만 놔둔채 실행하면 비밀변호변경페이지를 어드민페이지로 넘기기때문에 조정필요
    template_name = "users/update-password.html"