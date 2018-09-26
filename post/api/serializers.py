from rest_framework.serializers import (
    ModelSerializer ,
    HyperlinkedIdentityField,
    SerializerMethodField)

from post.models import PostModel

# from comment/api
from comment.api.serializers import CommentListSerializer
from comment.models import CommentModel


# serializers work like a ModelForm


class PostListSerializer(ModelSerializer):

    # this is a url hyperlink to the detail api view of a specific post,
    # work something like "get_absolutely_url" for detailview.
    #https://www.youtube.com/watch?v=vioDE-R6dNw&index=14&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS
    url_detail = HyperlinkedIdentityField(view_name ='post-api:post_api_detail', lookup_field='pk')
    url_update = HyperlinkedIdentityField(view_name ='post-api:post_api_update', lookup_field='pk')
    url_delete = HyperlinkedIdentityField(view_name ='post-api:post_api_delete', lookup_field='pk')

    # purpose of SerializerMethodField() is to show the username of the user,
    # without the SerializerMethodField the user will display in id, exp: "user":"3",
    # https://www.youtube.com/watch?v=KIws2te7kl8&index=15&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS
    user = SerializerMethodField()

    class Meta:
        model = PostModel
        fields = ['url_detail','url_update','url_delete', 'user','title']

    # the attribute of SerializerMethodField()
    def get_user(self, obj):
        return str(obj.user.username)


class PostDetailSerializer(ModelSerializer):

    user = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = PostModel
        fields = ['user', 'title', 'file', 'description','created_at','update_at','comments']

    # https://www.youtube.com/watch?v=kWTILxJ13xc&index=18&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS
    def get_comments(self,obj):
        content_type = obj.get_content_type
        object_id = obj.id
        comments_qs = CommentModel.objects.filter_by_instance(obj)
        comments = CommentListSerializer(comments_qs, many =True, context=self.context).data
        return comments

    def get_user(self, obj):
        return str(obj.user.username)

class PostUpdateCreateSerializer(ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['title', 'file', 'description']

class PostDeleteSerializer(ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['user', 'title', 'file', 'description','created_at','update_at']
