from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


# Follow user toggle manager
# https://www.youtube.com/watch?v=yDv5FIAeyoY&t=23608s 'at time 7:08:32'
class UserExtraModelManager(models.Manager):
    def toggle_follow(self, request_user, username_to_toggle):
        get_profile = UserExtraModel.objects.get(user__username__iexact = username_to_toggle)
        user = request_user
        is_following = False
        if user in get_profile.follower.all():
            get_profile.follower.remove(user)
        else:
            get_profile.follower.add(user)
            is_following = True
        return get_profile, is_following



class UserExtraModel(models.Model):
    #inherit the User model pk
    # the related name is use for the model that you get ForeignKey inherit the field inside this models
    user = models.OneToOneField(User, on_delete = models.CASCADE ,related_name = 'userextramodel')
    follower = models.ManyToManyField(User,blank=True, related_name ='is_following')
    image = models.ImageField(upload_to='profile_pics', blank=True)
    description = models.CharField(max_length= 250,default= '')
    city = models.CharField(max_length=250,default= '')
    website = models.URLField(blank= True,default= '')
    contact = models.CharField(max_length=100, blank= True,default= '')

    objects = UserExtraModelManager()

    def __str__(self):
        return self.user.username

# we will now define signals so our Profile model will be automatically created/updated
# when we create/update User instances.
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        # "instance" means the new user that register
        new_user = UserExtraModel.objects.create(user=instance)

        # Follow User
        # How to make super user Auto following every new user when they create their account
        # https://www.youtube.com/watch?v=yDv5FIAeyoY&t=23608s "Follow Users (6:33:28)"
        # first, get the super_user
        super_user = UserExtraModel.objects.get(user__username='giam')
        # second, add the "instance" also = "new_user" to our super_user every time when they is a new user register
        super_user.follower.add(instance)

        # Auto following 'super_user' when new_user create account/profile
        instance_user_profile = UserExtraModel.objects.get(user=instance)
        instance_user_profile.follower.add(super_user.user)

        # Auto following themself when they create/register a account
        instance_user_profile = UserExtraModel.objects.get(user=instance)
        instance_user_profile.follower.add(instance_user_profile.user)
post_save.connect(create_profile, sender = User)
