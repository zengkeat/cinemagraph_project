from django.shortcuts import render, get_object_or_404, redirect , HttpResponseRedirect
from django.views import generic
from .models import PostModel
from comment.models import CommentModel
from .forms import PostForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from comment.forms import CommentForm
from django.db.models import Q

# for GCBV message mixin
from django.contrib.messages.views import SuccessMessageMixin

# for checking if the user is login and authenticated
from django.contrib.auth.mixins import LoginRequiredMixin

#ContentType for comment
from django.contrib.contenttypes.models import ContentType


class PostView(SuccessMessageMixin,LoginRequiredMixin,generic.CreateView):
    model = PostModel
    fields = ['title','file','description']

    # GCBV MESSAGE EXAMPLE:https://stackoverflow.com/questions/24914637/show-a-successful-message-with-class-based-views
    success_message = 'Post create succesfully!'

    template_name = 'post/post.html'
    # the default template tag name of the CreateView and UpdateView in the html file is (form)

    # this line tell the form create by CreateView where to go if you dont want go
    # for the default get_absolute_url to see the detail after you posting.
    # example go to 'home'.
    # success_url = reverse_lazy('home')

    def form_valid(self, form):

        # NEWEST AND CLEAREST WAY. ANY ForeignKey ASOCIATED WITH THE Model
        # MUST USE THE METHOD OF SIGNAL THE USER MODEL
        # https://docs.djangoproject.com/en/2.1/topics/class-based-views/generic-editing/
        form.instance.user = self.request.user
        return super(PostView, self).form_valid(form)

        #OR THE OLDER WAY

        # post= form.save(commit=False)
        # post.user = self.request.user
        # post.save()
        # return super(PostView, self).form_valid(form)

# USING FBV FOR UPDATE BECAUSE GCBV CANNOT DO UPDATE AND DELETE IN A SINGLE VIEW
# CHECKOUT https://rayed.com/posts/2018/05/django-crud-create-retrieve-update-delete/ TO review
# FBV AND GCBV PERFORM CRUD
def PostUpdate(request,pk):

    # need to get the particular pk of the post, because we using FBV not GCBV
    update_delete = get_object_or_404(PostModel, pk=pk)

    # how to perform two button in single form  #
    # https://stackoverflow.com/questions/866272/how-can-i-build-multiple-submit-buttons-django-form #
    form_update = PostForm(request.POST , request.FILES, instance = update_delete)
    if 'confirm_post' in request.POST:
        if form_update.is_valid():
            update = form_update.save(commit = False)
            update.user= request.user
            update.save()
            return redirect('/user_profile/profile/')
    elif 'confirm_delete' in request.POST:
        update_delete.delete()
        return redirect('/user_profile/profile/')
    else:
        form_update = PostForm(instance = update_delete)

        # PURPOSE USE FOR SHOWING THE ORIGINAL CREATE TIME OF THE POST
        post = PostModel.objects.filter(pk=pk)

        context = {'form_update': form_update ,'post':post}
    return render(request, 'post/post_update.html',context)



class PostList(generic.ListView):
    model = PostModel
    template_name = 'post/post_list.html'

    def get(self,request,*args,**kwagrs):
        queryset = PostModel.objects.all()

        # Search Posts mechanism
        # https://www.youtube.com/watch?v=eyAIAZr5Q3w&index=37&list=PLEsfXFp6DpzQFqfCur9CJ4QnKQTVXUsRy
        # "query = request.GET.get('q')" is to GET the result of <input name='q'> field in the index.html
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(user__username__icontains=query) |
            Q(description__icontains=query)
            )

        context = {'post_list': queryset }
        return render(request,self.template_name,context)




'''
IF U NEED TO CUSTOMIZE OR ADD ALOT OF FUCNTION IN THE VIEW, USING FBV IS BETTER

'''
def PostDetail(request,pk):
    post_detail = get_object_or_404(PostModel, pk=pk)

    # **COMMENT FUNCTIONALITY**
    # CHECKOUT CONDINGENTREPRENEUR ADVANCING BLOG:14-16 FOR CREATING FULL FUNCTIONALITY COMMENT
    initial_data = {
        "content_type": post_detail.get_content_type,
        "object_id" : post_detail.pk
    }
    comment_form = CommentForm(request.POST or None, initial = initial_data)
    if comment_form.is_valid():
        c_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model = c_type)
        obj_id = comment_form.cleaned_data.get('object_id')
        content_data = comment_form.cleaned_data.get('content')

        # set the parent_obj to None first, then check the parent_id exists or not for validation.
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None

        if parent_id:
            parent_qs = CommentModel.objects.filter(pk = parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = CommentModel.objects.get_or_create(
                                user = request.user,
                                content_type =  content_type,
                                object_id = obj_id,
                                content= content_data,
                                parent= parent_obj,
                            )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    #https://www.youtube.com/watch?v=cdduWAjeTD4&list=PLEsfXFp6DpzQB82YbmKKBy2jKdzpZKczn&index=14
    # Model Managers & Instance Methods
    comments = post_detail.comments

    context = {'post_detail':post_detail, 'comments':comments, 'comment_form': comment_form}
    return render(request, 'post/post_detail.html', context)


# like button with AJAX
# https://www.youtube.com/watch?v=pkPRtQf6oQ8&t=594s
class PostLikeToggle(generic.RedirectView):
    # overwrite the default funtion of RedirectView "get_redirect_url"
    def get_redirect_url(self, *args, **kwargs):
        # first, get the 'pk' of this Post from the url that link with this view
        pk = self.kwargs.get("pk")
        print(pk)
        # second, use the 'pk' to get the objects of this post
        obj = get_object_or_404(PostModel, pk=pk)

        # this line means go to the get_absolute_url of this 'pk' or detailpage of this Post
        url_ = obj.get_absolute_url()

        user = self.request.user
        if user.is_authenticated:
            if user in obj.like.all():
                obj.like.remove(user)
            else:
                obj.like.add(user)
        # third, after toggle the like, return to the 'url_', also means redirect to the detailpage of this post
        # by grabbing the 'pk' of this post and pass it through the get_absolute_url() at the models.py
        return url_
