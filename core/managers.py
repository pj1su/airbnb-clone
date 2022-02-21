from django.db import models


class CustomModelManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

    # get으로 접근 다른 메소드를 접근하려면 filter사용
