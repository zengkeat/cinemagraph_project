from rest_framework.serializers import (
    ModelSerializer ,
    HyperlinkedIdentityField,
    SerializerMethodField)

from comment.models import CommentModel

# serializers work like a ModelForm

# https://www.youtube.com/watch?v=1Ii5yZLS1Jc&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS&index=17
# in our comment.models "CommentManager" method, we already filter the parent comment, so when
# listing the comment, only tha parent comment or main comment will be show up, the children comment will not.
class CommentListSerializer(ModelSerializer):

    url_detail = HyperlinkedIdentityField(view_name = 'comment-api:comment_api_detail', lookup_field='pk')
    url_update = HyperlinkedIdentityField(view_name = 'comment-api:comment_api_update', lookup_field='pk')

    # purpose of SerializerMethodField() is to show the username of the user,
    # without the SerializerMethodField the user will display in id, exp: "user":"3",
    # https://www.youtube.com/watch?v=KIws2te7kl8&index=15&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS
    user = SerializerMethodField()
    replies_count = SerializerMethodField()

    class Meta:
        model = CommentModel
        fields = ['url_detail','url_update','id','user','content_type','object_id','parent','replies_count']

    # the attribute of SerializerMethodField()
    def get_user(self, obj):
        return str(obj.user.username)

    # count how many reply
    # https://www.youtube.com/watch?v=1Ii5yZLS1Jc&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS&index=17
    def get_replies_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

class CommentDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    replies = SerializerMethodField()
    replies_count = SerializerMethodField()

    class Meta:
        model = CommentModel
        fields = ['id','user','content_type','object_id','content','timestamp','replies_count','replies']

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True,context=self.context).data

    def get_user(self, obj):
        return str(obj.user.username)

    # count how many reply
    # https://www.youtube.com/watch?v=1Ii5yZLS1Jc&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS&index=17
    def get_replies_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentUpdateSerializer(ModelSerializer):
    user = SerializerMethodField()
    class Meta:
        model = CommentModel
        fields = ['id','user','content','timestamp']

    def get_user(self, obj):
        return str(obj.user.username)




class CommentChildSerializer(ModelSerializer):
    user = SerializerMethodField()
    url_update = HyperlinkedIdentityField(view_name = 'comment-api:comment_api_update', lookup_field='pk')
    class Meta:
        model = CommentModel
        fields = ["url_update",'id','user','parent','content','timestamp']

    def get_user(self, obj):
        return str(obj.user.username)
