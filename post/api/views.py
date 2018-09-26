from rest_framework.generics import (
    ListAPIView ,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly)

from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostUpdateCreateSerializer,
    PostDeleteSerializer)

from post.models import PostModel
from .permissions import IsOwnerOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter




class PostListAPIView(ListAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostListSerializer
    # https://www.youtube.com/watch?v=aWTYoWFrrh8&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS&index=12
    # for searching mechanism at the url "http://127.0.0.1:8000/api/post/?search=(first_name),(title),(id)"
    # "http://127.0.0.1:8000/api/post/?search=giam" or "http://127.0.0.1:8000/api/post/?search=what does"
    # or add "&ordering=-user" then you can order the thing u search
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ['id','title','user__first_name']


class PostDetailAPIView(RetrieveAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostDetailSerializer
    # in default, urls.py will lookup to the pk or id field.
    # lookup_field = 'slug' (if you have a slug field instead of pk )

# purpose of "RetrieveUpdateAPIView" is to fill the field with information
# that you want to update, if just "UpdateAPIView", the field will be blank.
class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostUpdateCreateSerializer
    #https://www.youtube.com/watch?v=-0c88d24qzM&index=11&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS
    # we created IsOwnerOrReadOnly at the permissions.py file for only objects owner can
    # overwrite their own object
    permission_classes = [IsOwnerOrReadOnly]

class PostDeleteAPIView(DestroyAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostDeleteSerializer
    permission_classes = [IsOwnerOrReadOnly]

class PostCreateAPIView(CreateAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostUpdateCreateSerializer

    # this part mean save the creation/post to the user whoever currently sign in
    # https://www.youtube.com/watch?v=8-hJeWQgYTQ&index=10&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
