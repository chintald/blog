import graphene
from graphene_django import DjangoObjectType
from users.models import User, Profile

#Schema for User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "email", "username")

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ("id", "about_me", "image", "user")


class Query(graphene.ObjectType):
    pass