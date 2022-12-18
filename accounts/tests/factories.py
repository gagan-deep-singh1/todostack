import factory
import faker

from factory import SubFactory
from factory.django import DjangoModelFactory

from accounts.models import User
from common.tests.factories import DjangoUserFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    system_user = SubFactory(
        DjangoUserFactory,
        username=factory.LazyAttribute(lambda _: str(faker.Faker().email().lower())),
    )
