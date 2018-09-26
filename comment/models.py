from django.db import models
from django.contrib.auth.models import User
from article.models import ArticleModel
#generic ForeignKey
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Model Managers & Instance Methods FOR CREATE AND DISPLAY COMMENT
# https://www.youtube.com/watch?v=cdduWAjeTD4&list=PLEsfXFp6DpzQB82YbmKKBy2jKdzpZKczn&index=14
class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager,self).filter(parent =None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.pk
        # qs = "super(CommentManager, self)" == "CommentModel.objects"
        qs = super(CommentManager, self).filter(content_type=content_type, object_id = obj_id).filter(parent=None)
        return qs


class CommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # post = models.ForeignKey(PostModel,on_delete=models.CASCADE)
    # article = models.ForeignKey(ArticleModel,on_delete=models.CASCADE)

    #generic ForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey("self", null=True, blank = True, on_delete = models.CASCADE)

    content = models.TextField()
    timestamp =models.DateTimeField(auto_now_add = True)

    objects = CommentManager()

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-timestamp']

    # https://www.youtube.com/watch?v=KrGQ2Nrz4Dc&list=PLEsfXFp6DpzQB82YbmKKBy2jKdzpZKczn&index=16
    def children(self): # REPLY FUCNTION
        return CommentModel.objects.filter(parent=self).order_by('timestamp')

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
