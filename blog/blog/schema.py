from dataclasses import fields
import graphene
from graphene_django import DjangoObjectType

from core.models import Tag, Post, Comment
from users.models import User, Profile


# Schema for post



class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ("id", "name")

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "title", "slug", "author", "content", "image", "tags", "created_on", "updated_on")


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "name", "email", "content", "post", "created")


#Schema for User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "email", "username")

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ("id", "about_me", "image", "user")

#Query

class Query(graphene.ObjectType):

    #For Posts
    all_posts = graphene.List(PostType)
    post_by_title = graphene.Field(PostType, title=graphene.String())
    post_by_slug = graphene.Field(PostType, slug=graphene.String())
    # post_by_author = graphene.List(PostType, author=graphene.String())
    post_by_tag = graphene.List(TagType, tag=graphene.String())
    # posts_created_on = 
    # posts_updated_on =

    #For Users
    user = graphene.List(UserType)
    user_id = graphene.Field(UserType, id=graphene.String())
    user_email = graphene.Field(UserType, email=graphene.String())
    user_username = graphene.Field(UserType, username=graphene.String())
        
    def resolve_all_posts(root, info):
        return(
            Post.objects.prefetch_related("tags")
            .select_related("author").all()
        )

  
    def resolve_post_by_slug(root, info, slug):
        return(
            Post.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )

    # def resolve_post_by_author(root, info, author):
    #     return (
    #         Post.objects.prefetch_related("tags")
    #         .select_related("author")
    #         .filter(author__user__username=author)
    #     )

    def resolve_post_by_tag(root, info, tag):
        return (
            Tag.objects.prefetch_related("tags")
            .select_related("author")
            .filter(tags__name__iexact=tag)
        )

    #for UserType
    def resolve_user_username(root, info, username):
        return(
            User.objects.prefetch_related("tags")
            .select_related("author"
            .get(username=username))
        )
    
    def resolve_user_id(root, info, id):
        return(
            User.objects.get(id=id)
        )

    def resolve_user_email(root,info, email):
        return(
            User.objects.get(email=email)
        )



schema = graphene.Schema(query=Query)