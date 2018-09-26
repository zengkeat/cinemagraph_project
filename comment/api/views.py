from rest_framework.generics import (
    ListAPIView ,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    )

from rest_framework.mixins import(
    UpdateModelMixin,
    DestroyModelMixin
    )

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly)

from .serializers import (
    CommentListSerializer,
    CommentDetailSerializer,
    CommentUpdateSerializer,
)

from comment.models import CommentModel
from post.api.permissions import IsOwnerOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter




class CommentListAPIView(ListAPIView):
    queryset = CommentModel.objects.all()
    serializer_class = CommentListSerializer
    # https://www.youtube.com/watch?v=aWTYoWFrrh8&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS&index=12
    # for searching mechanism at the url "http://127.0.0.1:8000/api/post/?search=(first_name),(title),(id)"
    # "http://127.0.0.1:8000/api/post/?search=giam" or "http://127.0.0.1:8000/api/post/?search=what does"
    # or add "&ordering=-user" then you can order the thing u search
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ['user__username','user__first_name','content']


class CommentDetailAPIView(RetrieveAPIView):
    queryset = CommentModel.objects.all()
    serializer_class = CommentDetailSerializer
    # in default, urls.py will lookup to the pk or id field.
    # lookup_field = 'slug' (if you have a slug field instead of pk )

# Update & Destroy Mixins
# https://www.youtube.com/watch?v=DX3ekF1Xx8U&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS&index=22
class CommentUpdateAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = CommentModel.objects.filter(id__gte=0)
    serializer_class = CommentUpdateSerializer

    # "def put()" method is the built-in method for all the APIView that handle any kind of put(update/edit)
    def put(self, request, *args, **kwargs):
        #self.update is come from UpdateModelMixin
        return self.update(request, *args, **kwargs)

    # "def delete()" is the built-in method for all the APIView that handle specific for delete(destroy)
    def delete(self, request, *args, **kwargs):
        #self.destroy is come from DestroyModelMixin
        return self.destroy(request, *args, **kwargs)
