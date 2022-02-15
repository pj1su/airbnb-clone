import os
import requests
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import models, mixins
from django.core.files.base import ContentFile
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

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
class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    # success_url = reverse_lazy("core:home")
    # initial = {"email": "wltn5055@naver.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):  # class LogouView도 있음 document
    logout(request)
    messages.info(request, "See you later")
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm  # 더 확장하고싶으면 forms.SignupForm사용 , UserCreationForm
    success_url = reverse_lazy("core:home")
    # initial = {
    #     "first_name": "jisu",
    #     "last_name": "pakr",
    #     "email": "wltn8223@gmail.com",
    # }

    def form_valid(self, form):  # form에 user을 저장x
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            # 이부분에 send_email할 수 있지만 이메일 변경이나 재사용을 고려해서 모델에 재사용가능한 코드를 만듬
            user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # 나중에 성공메세지 추가
    except models.User.DoesNotExist:
        # 나중에 에러메세지 추가
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


# scope는 string이니까 그냥 넣는것
# github document에 소셜로그인 하는방법 인자넣는 순서 방법 나와있음
class GithubException(Exception):
    pass


# post로 받는경우 requests 로 받기
def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            # print(token.json())
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get access token")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                # print(profile_json)
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    name = username if name is None else name
                    email = profile_json.get("email")
                    email = name if email is None else email
                    bio = profile_json.get("bio")
                    bio = "" if bio is None else bio
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method == models.User.LOGIN_GITHUB:
                            # 로그인을 시도하다 #17.4 5:50초 코드 조금 간단하게 하느것도 참고
                            login(request, user)
                            messages.success(request, f"Welcome {user.first_name}님")
                        else:
                            raise GithubException(
                                f"please log in with:{user.login_method}"
                            )  # password or Kakao login 상황
                    except models.User.DoesNotExist:
                        new_user = models.User.objects.create(
                            username=email,
                            first_name=name,
                            bio=bio,
                            email=email,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        new_user.set_unusable_password()
                        new_user.save()
                        login(request, new_user)
                        messages.success(request, f"Welcome {user.first_name}님")
                    return redirect(reverse("core:home"))
                    # user = models.User.objects.get(email=email)
                    # if user is not None:
                    #     return redirect(reverse("users:login"))
                    # else:
                    #     user = models.User.objects.create(
                    #         username=email, first_name=name, bio=bio, email=email
                    #     )
                    #     login(request, user)
                    #     return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your profile")
                # print(api_request.json())
        else:
            raise GithubException("Can't get code")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    REST_API_KEY = os.environ.get("KAKAO_ID")
    REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code&scope=account_email,profile_nickname,profile_image"
        # &scope=account_email,profile_nickname,profile_image 로 필수로 추가할 수 있다
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        REST_API_KEY = os.environ.get("KAKAO_ID")
        REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}"
        )
        # print(token_request.json())
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get access token")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        # print(profile_request.json())
        profile_json = profile_request.json()
        email = profile_json.get("kakao_account").get("email", None)
        if email is None:
            raise KakaoException("email in None")
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"please log in with:{user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                username=email,
                email=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                # photo_request.content()  # json ,text도 아닌 0,1 과 같은 byte처럼 모든것을 의미
                user.avatar.save(
                    f"{nickname}-avatar.jpg",
                    ContentFile(
                        photo_request.content
                    ),  # byte로 된건 불러올수 없어서 ContentFile로 사용
                )
        login(request, user)
        messages.success(request, f"Welcome {user.first_name}님")
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"  # 이걸 지정안하면 룸 디테일에 룸호스트를 누르면 그룸의 사용자로 로그인된다 유저디테일 템플릿에서 user. 으로하면 모든 룸의 유저든 모두 바뀔 수 있으니 context지정후 써야함


# 이걸 지정할땐 유저모델에 앱솔루트 지정해서 pk인자값 받아오게

# url에서 pk를 받지 않기떄문에 get object를 써서 우리가 수정하기를 원하는 객체를 반환
class UpdateUserView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        # "email",
        # "username",  username을 밑에 폼 벨리드로 인터셉트가능 이메일이랑 유저네임 같게 하고싶은데 유저들한테 안보이게 할려면
        "first_name",
        "last_name",
        # "avatar",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )
    success_message = "Profile update"
    # placeholder사용하려면 modelForm사용헤야함
    def get_object(
        self, queryset=None
    ):  # 수정하고싶은 객체 반환 self , url에 int:pk가 없지만 유저를 줄때 ex) "update/"
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate"}
        return form

    # def form_valid(self, form):
    #     email = form.cleaned_data.get("email")
    #     self.object.username = email
    #     self.object.save()
    #     return super().form_valid(form)


class UpdatePasswordView(
    mixins.LoggedInOnlyView, SuccessMessageMixin, PasswordChangeView
):
    # pass 만 놔둔채 실행하면 비밀변호변경페이지를 어드민페이지로 넘기기때문에 조정필요
    template_name = "users/update-password.html"
    success_message = "Password update"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "old password"}
        return form

    # F12 눌러서 html에 input name 확인해서 필드명 알수있음
    # form valid는 폼 검증 get context사용할 데이터추가 form get 폼에서 데이터 더 추가가능

    def get_success_url(self):  # logic이 필요할땐 메소드 사용
        return self.request.user.get_absolute_url()