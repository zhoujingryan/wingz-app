from rest_framework import serializers

from wingz_sso.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "role")


def run(*args):
    try:
        email, password, role = args
    except ValueError:
        print("expect 3 arguments: email, password, role")
        print("abort!")
        return
    data = {"email": email, "password": password, "role": role}
    serializer = UserCreateSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create_user(**data)
    print(f"create user id={user.id_user},{email=} success!")
