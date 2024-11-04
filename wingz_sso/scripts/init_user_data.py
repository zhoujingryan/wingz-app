import random

from django_fakery.faker_factory import factory

from wingz_sso.constants import UserRole
from wingz_sso.models import User


def run(*args):
    try:
        count, *_ = args
        count = int(count)
    except ValueError:
        count = 100

    fake = factory.fake
    user_bp = factory.blueprint(User).fields(
        role=UserRole.REGULAR,
        first_name=lambda i, _: fake.first_name(),
        last_name=lambda i, _: fake.last_name(),
        email=lambda i, _: f"{fake.user_name()}{''.join(fake.words(random.randint(0, 3)))}@{fake.domain_name()}",
    )
    users = user_bp.b(quantity=count)()
    User.objects.bulk_create(users, batch_size=1000)
