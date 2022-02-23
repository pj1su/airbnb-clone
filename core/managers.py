from django.db import models
from django.contrib.auth.models import UserManager


class CustomModelManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

    # get으로 접근 다른 메소드를 접근하려면 filter사용


class CustomUserManager(CustomModelManager, UserManager):
    pass


# user 모델에서도 쓰기위해서

# 1. 먼저 Manager에 대해 : 기본적으로 모든 장고 model에는 manager가 objects라는 이름으로 기본 제공되며, 필요한 경우 커스텀할 수 있습니다. 니꼬샘은 이 커스텀한 manager를 core > managers.py에 모아서 저장했습니다.

# 2. room이나 reservation모델은 TimeStampedModel을 상속받고 , user는 AbstractUser를 상속받습니다
# 2-1) 상속받은 TimeStampedModel 에는 CustomModelManager이 이미 선언되어 있어요. objects = managers.CustomModelManager()
# 2-2) 상속받은 AbstractUser 에는 기본 UserManager이 선언되어 있으나, 커스텀 manager는 선언되어 있지 않습니다. objects = UserManager()

# 3. 따라서 user모델의 커스텀 manager를 사용하기 위해서는 user모델에 objects = core_managers.CustomUserManager()라고 별도로 선언을 해야, get_or_none메서드를 사용할수 있고, room이나 reservation모델에서는 이미 부모클래스에서 커스텀 manager가 선언되어 있었으므로, 바로 get_or_none메서드를 사용할 수 있었습니다.