from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from article.models import ArticleModel

from django.contrib.auth.models import User
from django.db.models import Q

class HomeView(TemplateView):
    template_name = 'index.html'

    # IN THE GCBV IS NOT SUITABLE FOR CREATE queryset = ArticleModel.objects.all() OUTSIDE
    # OF THE get() method, but you can do it in raw CBV
    # BECAUSE IF YOUR queryset = .. is outside the get() method, the page content will not refresh
    # after you apdated.
    def get(self, request,*args,**kwargs):
        queryset = ArticleModel.objects.all()

        # Search Posts mechanism
        # https://www.youtube.com/watch?v=eyAIAZr5Q3w&index=37&list=PLEsfXFp6DpzQFqfCur9CJ4QnKQTVXUsRy
        # "query = request.GET.get('q')" is to GET the result of <input name='q'> field in the index.html
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(user__username__icontains=query) |
            Q(description__icontains=query) |
            Q(content__icontains=query)
            )

        context = {'article_list':queryset }
        return render(request,self.template_name, context)
