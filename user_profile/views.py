from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView, View
from user_profile.forms import EditForm, UserExtraForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect


#listview
from post.models import PostModel
from article.models import ArticleModel
from django.contrib.auth.models import User
from .models import UserExtraModel



class UserProfileView(TemplateView):
    template_name = "user_profile/profile.html"

    def get(self,request):
        # ** RAW LISTVIEW **
        # this line grab all the objects in the PostModel and filter it by the user who currently using
        # or login
        # https://stackoverflow.com/questions/38471260/django-filtering-by-user-id-in-class-based-listview
        user_post_list = PostModel.objects.filter(user= self.request.user)
        user_post_article = ArticleModel.objects.filter(user = self.request.user)
        user_follower_count = UserExtraModel.objects.get(user = self.request.user)
        user_following_count = User.objects.get(username = self.request.user)
        context = { 'user_post_list': user_post_list,
                    'user_post_article':user_post_article,
                    'user_follower_count' :user_follower_count,
                    "user_following_count": user_following_count,}
        return render(request,self.template_name,context)



# this function (request) can access the user profile that login, so type
# {'user':request.user} can access the data of the user.
# if you just want to access the pk, we can type  user_dict = {'user':request.user.pk}
# https://www.youtube.com/watch?v=NhNmQcnv1ms&list=PLw02n0FEB3E3VSHjyYMcFadtQORvl1Ssj&index=17
def UserProfile(request):
     user_dict = {'user':request.user}
     return render(request,'user_profile/profile.html',user_dict)

def UserProfileEdit(request):

    if request.method == 'POST':
        form_edit = EditForm(request.POST, instance= request.user)

        # instance = request.user.userextraprofile mean pass the input to form_extra
        # if you want to save any file or images, must have request.FILES THEN EVERYTHING WILL BE OK!
        form_extra = UserExtraForm(request.POST, request.FILES ,instance= request.user.userextramodel)

        if form_edit.is_valid() and form_extra.is_valid():
            form_edit.save()
            form_extra.save()
            return redirect('/user_profile/profile')
    else:

        form_edit = EditForm(instance = request.user)
        # the purpose instance = request.user.userextraprofile is to fill out the field with data that
        #get from that database with the partiular user that currently using.
        form_extra = UserExtraForm(instance = request.user.userextramodel)
        user_edit = {'form_edit':form_edit,'form_extra':form_extra}
    return render(request,'user_profile/profile_edit.html',context=user_edit)


# Follow Button view
# we handle the logic in "ProfileFollowerToggle" instead of inside "UserProfileDetail" because you cant get the correct
# username with "user_to_toggle = request.POST.get("username")" in the "UserProfileDetail".
# if you handle the logic in "UserProfileDetail", yours **request.POST.get("username")** will run throught one time first
# and get the result of 'None' before clicking the follow-btn, result-in you cant get the "username" of the user that you to follow.
# **So handle the logic with creating a new "View" WILL LEAD THE "username" THAT YOU WANT TO GET PASSING THROUGH THE "URL" EVENTUALLY
# TO THIS "ProfileFollowerToggle" View. **
class ProfileFollowerToggle(View):

    # https://www.youtube.com/watch?v=yDv5FIAeyoY&t=23608s "Follow Button Form (6:53:30)"
    def post(self,request, *args,**kwargs):
        username_to_toggle = request.POST.get("username")
        get_profile, is_following = UserExtraModel.objects.toggle_follow(request.user, username_to_toggle)
        return redirect(f'/user_profile/{get_profile.user.id}')


def UserProfileDetail(request,pk):

    # link all the user post and article with "related_name" in the PostModel
    # and ArticleModel
    user_info = get_object_or_404(User, pk=pk)
    context ={}
    context['user_info'] = user_info
    context['request_user'] = request.user.username


    # **the purpose of authenticated "request.user" is to avoid error when non-user get into the
    # UserProfileDetail page. Because without login,
    # django dont know who is request.user and it will raising error **
    if request.user.is_authenticated == True :

    # the purpose of this part is to verify the "user_info objects" is being following by the "request.user" anot
    # and get the result to put it in the form for toggle between "Follow" and "Unfollow".
    # https://www.youtube.com/watch?v=yDv5FIAeyoY&t=23608s "Follow Button Form (6:53:30)"
        is_following = False
        if user_info.userextramodel in request.user.is_following.all():
            is_following = True
            context['is_following'] = is_following

    return render(request, 'user_profile/profile_detail.html', context)

# Follower HomeFeed
# https://www.youtube.com/watch?v=yDv5FIAeyoY&t=23608s (43 - Following Home Page Feed (7:12:55))
class HomeFeedView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        is_following_user_id = [x.user.id for x in user.is_following.all()]
        '''
        list=[]
        for x in user.is_following.all():
            list.append(x.user.id)
        '''
        Post_feed = PostModel.objects.filter(user__id__in = is_following_user_id).order_by('-update_at')[:7] # "[:7]" means limit the number of post at 7
        Article_feed = ArticleModel.objects.filter(user__id__in = is_following_user_id).order_by('-updated')[:7]

        context = {'Post_feed':Post_feed, 'Article_feed':Article_feed}
        return render(request, 'user_profile/HomeFeed.html', context)


class FollowerView(View):

    # this part get the request.POST from the profile.html "follower form" throught url that link to 
    # this particular view to process it
    def post(self, request, *args, **kwargs):
        context = {}
        if "follower" in request.POST:
            follower = UserExtraModel.objects.get(user = self.request.user)
            all_follower = follower.follower.all()
            context['all_follower'] = all_follower
        elif "following" in request.POST:
            user = User.objects.get(username = self.request.user)
            all_following = user.is_following.all()
            context['all_following'] = all_following
        # elif 'username' in request.POST:
        #     # print(request.POST)
        #     # print(request.POST.get('username'))
        #     username_to_toggle = request.POST.get("username")
        #     get_profile, is_following = UserExtraModel.objects.toggle_follow(request.user, username_to_toggle)
        #     return redirect('home')
        return render(request,'user_profile/follower.html',context)
