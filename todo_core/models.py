from django.db import models

from accounts.models import User
from common.models import AbstractModel


# Create your models here.


class TodoItem(AbstractModel):
    PRIORITY_LOW = 0
    PRIORITY_MEDIUM = 1
    PRIORITY_HIGH = 2

    PRIORITY_CHOICES = (
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="todo_items",
        help_text="Owner of the todo item",
    )

    title = models.CharField(
        max_length=200, help_text="Represents the title of the todo item"
    )
    description = models.TextField(
        help_text="Represents the description of the todo item"
    )

    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=PRIORITY_LOW,
        help_text="Represents the priority of the todo item",
    )

    due_date = models.DateTimeField(
        null=True, blank=True, help_text="Represents the due date of the todo item.",
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Represents the date and time when the todo item was completed",
    )

    class Meta(AbstractModel.Meta):
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

    @classmethod
    def get_for_user(cls, user):
        return cls.objects.filter(owner=user).order_by("-created_at")
