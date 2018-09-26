from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.views import View
from .forms import ArticleForm
from .models import ArticleModel
from django.contrib.auth.models import User
from django.urls import reverse


# for GCBV message mixin
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.mixins import LoginRequiredMixin


# **USING RAW CLASS BASED VIEW (CBV)**
# ** USING RAW CBV IN THIS APPLICATION JUST TO LEARN THE MOST RAW WAY ABOUT CRUD AND UNDERSTAND
# MORE ABOUT THE CBV AND THEIR BUILT IN METHOD( get(), get_object(), get_queryset(),post())**


# the usefulness of 'ArticleModelObjectMixin' is to reduce the redundancy in the code
# https://www.youtube.com/watch?v=SBopye4v1UA&list=PLEsfXFp6DpzTD1BD1aWNxS2Ep06vIkaeW&index=47
class ArticleModelObjectMixin(object):
    model = ArticleModel

    # purpose of get_object is to get the specific id or slug, mostly use for update, delete and detail
    # all the 'id' is change to 'slug' because we use slugfield instead of the id
    def get_object(self):
        slug = self.kwargs.get('slug')
        obj = None
        if slug is not None:
            obj = get_object_or_404(self.model , slug=slug)
        return obj


# RAW CREATEVIEW WITH (CBV)
# https://www.youtube.com/watch?v=uYj5VG0-nVQ&list=PLEsfXFp6DpzTD1BD1aWNxS2Ep06vIkaeW&index=43
class ArticleCreate(LoginRequiredMixin,View):
    template_name = 'article/article_create.html'
    form_class = ArticleForm

    # get() mean what is the content of the page need to show
    def get(self, request, *args, **kwargs):
        form_create = self.form_class()
        return render(request, self.template_name, {'form_create':form_create})

    # post() is get the result of the page and analyse it
    def post(self, request, id=None, *args, **kwargs):
        form_create = self.form_class(request.POST, request.FILES)
        if form_create.is_valid():
            create = form_create.save(commit = False)
            create.user = request.user
            create.save()

            # equivalent to: return HttpResponseRedirect(create.get_absolute_url())
            return redirect(create)

        return render(request, self.template_name, {'form_create':form_create})


# RAW UPDATEVIEW WITH CBV
# https://www.youtube.com/watch?v=oLrTvbvTWsg&index=45&list=PLEsfXFp6DpzTD1BD1aWNxS2Ep06vIkaeW
class ArticleUpdate(LoginRequiredMixin, ArticleModelObjectMixin,View):
    template_name = 'article/article_update.html'
    form_class = ArticleForm

    # no need this get_object() method because we have "ArticleModelObjectMixin"
    # def get_object(self):
    #     slug = self.kwargs.get('slug')
    #     obj = None
    #     if slug is not None:
    #         obj = get_object_or_404(ArticleModel, slug=slug)
    #     return obj

    # purpose of get() is what should server get and show in the page (method == GET)
    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form_update = self.form_class(instance = obj)
            # THIS "context['object'] = obj" IS TO GRAB THE DATA THEN WE
            # CAN USE IT FOR exp:'object.title' in html file
            context['object'] = obj
            context['form_update'] = form_update
        return render(request, self.template_name, context)

    # purpose of post() is post the result and save it (method == POST)
    def post(self, request, *args, **kwargs):
        context={}
        obj = self.get_object()
        if obj is not None:
            form_update = self.form_class(request.POST, request.FILES, instance= obj)

            if form_update.is_valid():
                update = form_update.save(commit = False)
                update.user = request.user
                update.save()
                return HttpResponseRedirect(update.get_absolute_url())

            context['object'] = obj
            context['form_update'] = form_update

        return render(request, self.template_name,context)


# DetailView with Raw CBV
# https://www.youtube.com/watch?v=Dj9dUICSil4&list=PLEsfXFp6DpzTD1BD1aWNxS2Ep06vIkaeW&index=41
class ArticleDetail(View):
    template_name = 'article/article_detail.html'

    # default id=None in get() change to slug=None, because our id is change to slug now!
    # if not, content inside the html wont show.
    def get(self, request, slug=None, *args, **kwargs):
        context = {}
        if slug is not None:
            obj = get_object_or_404(ArticleModel, slug=slug)
            context['object'] = obj
        return render(request,self.template_name,context)

    # ** OR ** USING 'ArticleModelObjectMixin'
    # def get(self, request, slug=None, *args, **kwargs):
    #     return render(request,self.template_name,{'object':self.get_object()})


# RAW DELETE CBV
# https://www.youtube.com/watch?v=mDsnX-uEXK0&list=PLEsfXFp6DpzTD1BD1aWNxS2Ep06vIkaeW&index=46
class ArticleDelete(LoginRequiredMixin,ArticleModelObjectMixin,View):
    template_name = 'article/article_delete.html'

    # no need this get_object() method because we have "ArticleModelObjectMixin"
    # def get_object(self):
    #     slug = self.kwargs.get('slug')
    #     obj = None
    #     if slug is not None:
    #         obj = get_object_or_404(ArticleModel, slug=slug)
    #     return obj

    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            # THIS "context['object'] = obj" IS TO GRAB THE DATA THEN WE
            # CAN USE IT FOR exp:'object.title' in html file
            context['object'] = obj
        return render(request, self.template_name, context)

    # purpose of post() is post the result and save it (method == POST)
    def post(self, request, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('/user_profile/profile/')
        return render(request, self.template_name,context)
