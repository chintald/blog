from email import contentmanager
from typing_extensions import Required
from urllib import request
import graphene
from graphene_django import DjangoObjectType
from core.models import Tag, Post, Comment
from users. models import User, Profile
from users.schema import UserType


#Schema for Tag Start
class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ("id", "name")
    
class CreateTag(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True )

    tag = graphene.Field(TagType)

    def mutate(self, root, name):
        tag = Tag.objects.create(
            name = name
        )
        tag.save()

        return CreateTag(
            tag = tag
        )

class UpdateTag(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        id = graphene.ID()

    tag = graphene.Field(TagType)

    def mutate(self, info,id, name=None):
        tag = Tag.objects.get(pk=id)
        tag.name = name if name is not None else tag.name

        tag.save()

        return UpdateTag(tag=tag)

  #No need of delete tag as the tags are defined by admin

class DeleteTag(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    tag = graphene.Field(TagType)

    def mutate(self, info, id):
        tag = Tag.objects.get(pk=id)
        if Tag is not None:
            tag.delete()
        
        return DeleteTag(tag=tag)

#Schema for Tag End

#Schema for Comment Start

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "name", "email", "content", "post", "created")

#### Have doubts regarding Comment mutations

class CreaeteComment(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        content = graphene.String(required=True)
        post_id = graphene.ID(required=True)
        

    comment = graphene.Field(CommentType)

    def mutate(self, root, name, email, content,post_id):
        post = Post.objects.get(id=post_id)
        if post is not None:
            comment = Comment.objects.create(
                name=name,
                email=email,
                content=content,
                post=post
            )
        comment.save()
        return CreaeteComment(
            comment = comment
        )
        

#Schema for Comment End



class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "title", "slug", "author", "content", "image", "tags", "created_on", "updated_on")


#Qery for whole schema

class Query(graphene.ObjectType):

    #For Posts

    all_posts = graphene.List(PostType)
    post_by_title = graphene.Field(PostType, title=graphene.String())
    post_by_slug = graphene.Field(PostType, slug=graphene.String())
    post_by_tag = graphene.List(TagType, tag=graphene.String())
    post_author = graphene.Field(UserType, author=graphene.String())
    post_content = graphene.Field(PostType, content=graphene.String())
    post_created_on = graphene.Field(PostType, created_on=graphene.String())
    post_updated_on = graphene.Field(PostType, updated_on=graphene.String())
        
    def resolve_all_posts(root, info):
        return(
            Post.objects.prefetch_related("tags")
            .select_related("author").all()
        )

    def resolve_post_author(root, info, author):
        return(
            User.objects.get(author=author) 
        )

    def resolve_post_by_slug(root, info, slug):
        return(
            Post.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )


    def resolve_post_by_tag(root, info, tag):
        return (
            Tag.objects.prefetch_related("tags")
            .select_related("author")
            .filter(tags__name__iexact=tag)
        )

    def resolve_post_content(root, info, content):
        return(
            Post.objects.get(content=content)
        )

    def resolve_post_created_on(root, info, created_on):
        return(
            Post.objects.get(created_on=created_on)
        )

    def resolve_post_updated_on(root, inof, updated_on):
        return(
            Post.objects.get(updated_on=updated_on)
        )
    
    #for comments
    all_comments = graphene.List(CommentType)
    comment_user_name = graphene.Field(CommentType, name=graphene.String())
    comment_user_email = graphene.Field(CommentType, email=graphene.String())
    comment_content = graphene.Field(CommentType, content=graphene.String())
    comment_post_title = graphene.Field(CommentType, post=graphene.String())
    comment_created_on = graphene.Field(CommentType, created=graphene.String())

    def resolve_all_comments(root, info):
        return(
            Comment.objects.all()
        )
        
    def resolve_comment_user_name(root, info, name):
        return(
            Comment.objects.get(name=name)
        )
    
    def resolve_comment_user_email(root, info, email):
        return(
            Comment.objects.get(email=email)
        )

    def resolve_comment_content(root, info, content):
        return(
            Comment.objects.get(content=content)
        )

    def resolve_post_title(root, info, post):
        return(
            Comment.objects.get(post=post)
        )

    def resolve_comment_created_on(root, info, created):
        return(
            Comment.objects.get(creaeted=created)
        )

    #For Tags
    all_tags = graphene.List(TagType)
    tag = graphene.Field(TagType, tag=graphene.String())

    def resolve_all_tags(root, info):
        return(
            Tag.objects.all()
        )

    def resolve_tag(root, info, tag):
        return(
            Tag.objects.get(name=tag)
        )


class Mutation(graphene.ObjectType):
    create_tag = CreateTag.Field()
    update_tag = UpdateTag.Field()
    delte_tag = DeleteTag.Field()
    create_comment = CreaeteComment.Field()
