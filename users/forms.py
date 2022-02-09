from django import forms
from . import models

# forms에 자동적으로 에러메세지 보여주는 기능이있다
class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # 두 개 다른 field가 서로 관련이 있을 때 확인하는 method
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):  # 비밀번호 암호화 된것들 서로 확인
                return self.cleaned_data  # cleaned 메소드쓰면 cleaned data 무조건 리턴
            else:  # raise처럼 모든곳에 에러 뜨게하기싫을때
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(username=email)
    #         return email
    #     except models.User.DoesNotExist:
    #         raise forms.ValidationError("User does not exist")

    # def clean_password(self):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #     try:
    #         user = models.User.objects.get(username=email)
    #         if user.check_password(password):
    #             return password
    #         else:
    #             raise forms.ValidationError("Password is wrong")
    #     except models.User.DoesNotExist:
    #         pass  # 에러가 2번생기니까 email에 에러메세지 이미 있음


class SignUpForm(forms.ModelForm):  # ModelForm은 model에 있는 필드들을 계속 들고오기 번거로울때 쓴다
    # ModelForm은 clean data , save , unique한 field값을 validate할 수 있다(유저가 맞는지 유저가 존재하는지 등등)
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    # first_name = forms.CharField(max_length=80)
    # last_name = forms.CharField(max_length=80)
    # email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    # password는 유저가 가지고있지 않으니 그냥 놔두는거 암호화니까

    # def clean_email(self): #ModelForm이 email을 clean시키니까
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(email=email)
    #         raise forms.ValidationError("User already exists with that email")
    #     except models.User.DoesNotExist:
    #         return email

    def clean_password1(
        self,
    ):  # 위에서 부터 차례대로 clean data하기때문에 맨끝에 있는 passoword1은 clean이 안돼서 나온다 그래서 에러 def clean_passowrd1 으로하면 전부 clean data한다
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("password confirmation does not match")
        else:
            return password

    # def save(self): ModelForm은 save method도 가지고있다. 하지만 username을 trick해야함
    #     first_name = self.cleaned_data.get("first_name")
    #     last_name = self.cleaned_data.get("last_name")
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #     password1 = self.cleaned_data.get("password1")

    #     ## models.User.objects.create() 암호화된 비밀번호를 저장할 수 없음.(생 데이터를 저장함)
    #     user = models.User.objects.create_user(email, email, password)
    #     user.first_name = first_name
    #     user.last_name = last_name
    #     user.save()
    def save(self, *args, **kwargs):
        # django save method overrid 내가 원하는대로 세이브 하기위해 자동으로 저장하면 username password가 없어도 저장되서
        # save(commit=False)를 적용한다면 django object는 생성되지만 object는 데이터베이스에 올라가지 않음
        user = super().save(
            commit=False
        )  # Call the real save() method 유저는 만들지만 저장하지말라 field에 있는 인스턴트들만 저장을 하기때문에 commit False로 인스턴스는 저장된 user을 만듬 그 후에 패스워드와 유저네임을 저장
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()
