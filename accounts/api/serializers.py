from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer ,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError,
    )

from django.contrib.auth.models import User
from django.db.models import Q


# serializers work like a ModelForm

# https://www.youtube.com/watch?v=B7bdoLMQrJY&index=25&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS
class AccountRegisterSerializer(ModelSerializer):

    # create another field because in default User model doesnt have the 'password2' field
    password2 = CharField(label='Confirm Password')

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','password2']

        # this line make the passsword unvisible after creating accounts
        extra_kwargs= {'password':{'write_only':True}}

    # Serializer Validation
    # validation of password2 manually
    # https://www.youtube.com/watch?v=5dtbbImcUCI&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS&index=27
    def validate_password2(self, value):
        # self.get_initial() mean get the initial data from the form that user insert
        data = self.get_initial()
        # get the password
        password1 = data.get('password')
        password2 = value
        # after that, compare it with password2
        if password1 != password2:
            raise ValidationError('Password must match!')
        return value


    # ModelSerializer Create Method
    # u need to add this method to successfully create user accounts using APIView that work when u login
    # without this function, your accout password cannot save correctly because of lack of hashing algorithem
    # https://www.youtube.com/watch?v=fvMLvFnEBBM&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS&index=26
    def create(self, validated_data):
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email  = email,
            )

        user_obj.set_password(password)
        user_obj.save()
        return validated_data



# Base APIView for User Login
# https://www.youtube.com/watch?v=gNXnDlfYOqA&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS&index=28
class AccountLoginSerializer(ModelSerializer):

    token = CharField(allow_blank=True, read_only=True)
    username = CharField()

    class Meta:
        model = User
        fields = ['username','password','token']

        # this line make the passsword unvisible after creating accounts
        extra_kwargs= {'password':{'write_only':True}}

    # UserLogin API Validation
    # https://www.youtube.com/watch?v=0jSzFUZ__k8&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS&index=29
    def validate(self, data):
        user_obj = None
        username = data.get('username')
        password = data['password']

        # first, get the data from username field and check did the user enter the username anot
        if not username:
            raise ValidationError('A username is required to login.')

        # if there is a username provided, grab the username and filter it with the User model Database
        # the function of "Q()" is to lookup something in the database; distinct() means incase if there is more than
        # one same username/objects, it only choose one, to avoid the duplicate
        user = User.objects.filter(Q(username = username)).distinct()

        # this line means if "user" exists and the queryset only contains one "user" object
        # the purpose of "user.count() == 1 " is to make sure it only get the right 'user' objects for the user that want to login.
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError('The username is bot valid.')

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError('Incorrect credetials please try again.')
        data['token']= 'SOME RANDOM TOKEN'
        return data




# class CommentDetailSerializer(ModelSerializer):
#     user = SerializerMethodField()
#     replies = SerializerMethodField()
#     replies_count = SerializerMethodField()
#
#     class Meta:
#         model = CommentModel
#         fields = ['id','user','content_type','object_id','content','timestamp','replies_count','replies']
#
#     def get_replies(self, obj):
#         if obj.is_parent:
#             return CommentChildSerializer(obj.children(), many=True,context=self.context).data
#
#     def get_user(self, obj):
#         return str(obj.user.username)
#
#     # count how many reply
#     # https://www.youtube.com/watch?v=1Ii5yZLS1Jc&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS&index=17
#     def get_replies_count(self, obj):
#         if obj.is_parent:
#             return obj.children().count()
#         return 0
#
#
# class CommentUpdateSerializer(ModelSerializer):
#     user = SerializerMethodField()
#     class Meta:
#         model = CommentModel
#         fields = ['id','user','content','timestamp']
#
#     def get_user(self, obj):
#         return str(obj.user.username)
#
#
#
#
# class CommentChildSerializer(ModelSerializer):
#     user = SerializerMethodField()
#     url_update = HyperlinkedIdentityField(view_name = 'comment-api:comment_api_update', lookup_field='pk')
#     class Meta:
#         model = CommentModel
#         fields = ["url_update",'id','user','parent','content','timestamp']
#
#     def get_user(self, obj):
#         return str(obj.user.username)
