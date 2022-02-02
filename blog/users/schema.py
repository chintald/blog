import email
from shutil import unregister_unpack_format
from xml.dom import UserDataHandler
import graphene
from graphene_django import DjangoObjectType
import users
from users.models import User, Profile

#Schema for User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "email", "username")

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = User.objects.create(
            username=username,
            email=email,
        )

        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class UpdateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        id = graphene.ID()

    user = graphene.Field(UserType)

    def mutate(self, info, id, username, password, email):
        user = User.objects.get(pk=id)
        user.username = username
        user.email = email

        user.set_password(password)
        user.save()

        return UpdateUser(user=user)


## Should not Delete user as it is not a nullable field 

# class DeleteUser(graphene.Mutation):
#     class Arguments:
#         id = graphene.ID()

#     user = graphene.Field(UserType)

#     def mutate(self, info, id):
#         user = User.objects.get(pk=id)
#         if user is not None:
#             user.delete()

#         return DeleteUser(user=user)


        



class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ("id", "about_me", "image", "user")

class CreateProfile(graphene.Mutation):
    profile = graphene.Field(ProfileType)

    class Arguments:
        about_me = graphene.String()
        user = graphene.String()
    
    def mutate(self, info, about_me, user):
        profile = Profile.objects.create(
            about_me=about_me,
            user=user
        )

        profile.save()

        return CreateProfile(profile=profile)

class UpdateProfile(graphene.Mutation):
    profile = graphene.Field(ProfileType)

    class Arguments:
        about_me = graphene.String()
        user = graphene.String()
        id = graphene.ID()

    profile = graphene.Field(ProfileType)

    def mutate(self, info, about_me, user, id):
        profile = Profile.objects.get(pk=id)

        profile.about_me = about_me
        profile.user = user

        profile.save()

        return UpdateProfile(profile=profile)


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    profile = graphene.List(ProfileType)

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_profile(self, info):
        return Profile.objects.all()



#Mutation Class

class Mutation(graphene.ObjectType):
    create_user =  CreateUser.Field()
    update_user = UpdateUser.Field()
    # delete_user = DeleteUser.Field()
    create_profile = CreateProfile.Field()
    update_profile = UpdateProfile.Field()