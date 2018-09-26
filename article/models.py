from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import FileExtensionValidator
# for ckeditor
from ckeditor_uploader.fields import RichTextUploadingField
from .utils import get_read_time


class ArticleModel(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'articlemodel')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique =True)
    description = models.CharField(max_length=300, blank= True)
    content = RichTextUploadingField(config_name = 'special', extra_plugins=['preview','autogrow'])# for adding plugin that already in default plugins set)
    # for extra ckeditor 5 plugin not inside the default
    # ,external_plugin_resources=[(
    #     'easyimage',
    #     '/static/ckeditor_tool/ckeditor/ckeditor/plugins/easyimage/',
    #     'plugin.js',
    # )],

    read_time = models.IntegerField(default = 0) # return a integer like 3 minutes or 30
    file = models.FileField(upload_to="article", validators=[FileExtensionValidator(allowed_extensions=['gif','png','jpg','jpeg','mp4'])],blank=True, null = True)
    updated = models.DateTimeField(auto_now = True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article:article_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp" ,"-updated" ]


    # add this when you have a file or image fields
    # for better approach which would not violate DRY is to add a helper method to the model class like:
    # https://stackoverflow.com/questions/15322391/django-the-image-attribute-has-no-file-associated-with-it
    @property
    def file_url(self):
        if self.file and hasattr(self.file, 'url'):
            return self.file.url
    # and use default_if_none template filter to provide default url:
    # <img src="{{ object.image_url|default_if_none:'#' }}" />

# create slug connect with id
# https://www.youtube.com/watch?v=Bmvd1O5pNIY
def create_slug(instance, new_slug = None):

    #create the slug for new post
    slug = slugify(instance.title)
    #check for the slug in the database for duplication, exp: if there is same title post
    if new_slug is not None:
        slug = new_slug
    qs = ArticleModel.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = '%s-%s' %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

# this pre_save_post_reciever function mean create or do something before saving data.
def pre_save_post_reciever(sender, instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    # Blog Post Read Time in Django:
    # https://www.youtube.com/watch?v=-8YN3_nlUFY&list=PLEsfXFp6DpzQB82YbmKKBy2jKdzpZKczn&index=20
    # id content field is True then
    if instance.content:
        # call the content inside the content field (by directly calling instance.fieldname) then resign it as html_string
        html_string = instance.content
        # after that, pass the html_string into get_read_time function
        read_time_result = get_read_time(html_string)
        # last, call the read_time field and asign it as the read_time_result
        instance.read_time = read_time_result

pre_save.connect(pre_save_post_reciever, sender=ArticleModel)
