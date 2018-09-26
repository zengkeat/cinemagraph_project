from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from comment.models import CommentModel

# for validation of file
from django.core.validators import FileExtensionValidator

#ContentType for comment
from django.contrib.contenttypes.models import ContentType

class PostModel(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'postmodel')
    title = models.CharField(max_length =200, unique = True)
    # auto_now_add mean only record the time when the post first time create
    created_at = models.DateTimeField(auto_now=False,auto_now_add = True)
    # auto_now mean create/update the time whenever the post being save
    update_at = models.DateTimeField(auto_now=True,auto_now_add = False)
    like = models.ManyToManyField(User, blank = True, related_name = 'post_likes')
    file = models.FileField(upload_to="post", validators=[FileExtensionValidator(allowed_extensions=['gif','png','jpg','jpeg','mp4'])])
    description = models.TextField()

    def __str__(self):
        return self.title

    # **get_absolute_url tell the server go to the particular post id or pk url, example(http://127.0.0.1:8000/post/23/),
    # in most of the cases, show the DetailView of the particular post.
    # If there is not success_url in CreateView or UpdateView, then in default in will go for get_absolute_url,
    # because most of the time we want to see our post after creating, which is in DetailView.
    # IT GUIDE THE SERVER TO THE DETAIL PAGE WHEN PARTICULAR ID OR PK IS CALL
    # THE post: in 'post:post_detail' is the namespace of the app, and the :post_detail is
    # the pk or id url name
    # https://www.youtube.com/watch?v=KB_wDXBwhUA&list=PLEsfXFp6DpzTD1BD1aWNxS2Ep06vIkaeW&index=38
    # https://www.youtube.com/watch?v=M5ytu6yzod0&t=467s
    def get_absolute_url(self):
        return reverse("post:post_detail", kwargs={"pk": self.pk})

    def get_like_url(self):
        return reverse("post:like_toggle", kwargs={"pk": self.pk})

    # to make the order based on the field you want
    class Meta:
        ordering = ["-created_at" ,"update_at" ,]
        verbose_name = "postmodel"

    ####################################
        ##  COMMENT FUNCTIONALITY ##
    ####################################
    # Model Managers & Instance Methods FOR DISPLAY Comment
    # https://www.youtube.com/watch?v=cdduWAjeTD4&list=PLEsfXFp6DpzQB82YbmKKBy2jKdzpZKczn&index=14
    @property
    def comments(self):
        instance = self
        qs = CommentModel.objects.filter_by_instance(instance)
        return qs

    # for creating comment
    # https://www.youtube.com/watch?v=zgF-KtQPqxQ&list=PLEsfXFp6DpzQB82YbmKKBy2jKdzpZKczn&index=15
    @property
    def get_content_type(self):
        instance = self
        qs = ContentType.objects.get_for_model(instance.__class__)
        return qs
