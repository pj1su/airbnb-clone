from django.shortcuts import render, redirect, reverse
from django.http import Http404
from users import models as user_models
from . import models
from django.views.generic import View
from django.db.models import Q

# from . import forms


def go_conversation(request, a_pk, b_pk):
    user_one = user_models.User.objects.get_or_none(pk=a_pk)
    user_two = user_models.User.objects.get_or_none(pk=b_pk)
    if user_one is not None and user_two is not None:
        try:
            conversation = models.Converation.objects.get(
                Q(participants=user_one) & Q(participants=user_two)
            )
            # conversation = models.Converation.objects.filter(participants=user_one).filter(participants=user_two) database적으로 좋지않음 필터를 2번해서
        except models.Converation.DoesNotExist:
            conversation = models.Converation.objects.create()
            conversation.participants.add(user_one, user_two)
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


# DetailView는 알아서 pk가져옴
class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Converation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        # form = forms.AddCommentForm
        return render(
            self.request,
            "conversations/converation_detail.html",
            {"converation": conversation},
            # "form": form
        )

    def post(self, *args, **kwargs):
        # form = forms.AddCommentForm(self.request.POST)
        # print(form)
        # print(self.request.POST) 폼없애고 인풋일때 이렇게 출력함
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = models.Converation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        if message is not None:
            models.Message.objects.create(
                message=message,
                user=self.request.user,
                converation=conversation,
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
        #render로 하면 self.reuqest해야함 자기자신한테 보내는거니
