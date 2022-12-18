from django.db import models

from common.models import AbstractModel
from django.contrib.auth.models import User as DjangoUser


class User(AbstractModel):
    system_user = models.OneToOneField(
        DjangoUser,
        on_delete=models.PROTECT,
        help_text="The django user linked to this user",
        related_name="todostack_user",
    )

    image = models.ImageField(default="default.png", upload_to="profile_pics")
