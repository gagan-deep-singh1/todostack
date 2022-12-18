from factory import DjangoModelFactory, Sequence, post_generation
from django.contrib.auth.models import User as DjangoUser


class DjangoUserFactory(DjangoModelFactory):
    class Meta:
        model = DjangoUser

    username = Sequence(lambda n: f"user_{n}")
    password = "test"
    first_name = "ßhamra"
    last_name = "ßhamra"
    email = "abc@xyz.com"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Override the default ``_create`` with our custom call.
        Due to internal behavior or create user create method that forces is_staff kwarg

        https://github.com/rbarrois/factory_boy/issues/132
        """

        manager = cls._get_manager(model_class)
        is_staff = kwargs.pop("is_staff", None)
        user = manager.create_user(*args, **kwargs)
        if is_staff:
            user.is_staff = is_staff
            user.save()
        return user

    @post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)
