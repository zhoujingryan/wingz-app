from django_fakery.faker_factory import factory

from wingz_sso.models import User


def run(*args):
    try:
        count, *_ = args
        count = int(count)
    except ValueError:
        count = 100

    users = factory.build(User, quantity=count)
    User.objects.bulk_create(users, batch_size=1000)
