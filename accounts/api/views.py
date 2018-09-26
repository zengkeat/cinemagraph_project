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

# for AccountLoginAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView


from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly)

from .serializers import (
    AccountRegisterSerializer,
    AccountLoginSerializer,
)

from django.contrib.auth.models import User
from post.api.permissions import IsOwnerOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter


class AccountRegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountRegisterSerializer
    permission_classes = [AllowAny]


# use normal APIView because this is login view, no need to create or update something, just want to POST something to DB.
# https://www.youtube.com/watch?v=gNXnDlfYOqA&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS&index=28
class AccountLoginAPIView(APIView):

    serializer_class = AccountLoginSerializer
    permission_classes = [AllowAny]

    # def post() in the rest_framework doesnt validate the data,
    # it just post the data to the database, not really validate the data.
    def post(self,request, *args ,**kwargs):
        # first, request the data from Login APiview first(the data that user type)
        data = request.data
        # second, passing the data throught the serializer
        serializer = AccountLoginSerializer(data = data)
        # third, check is_valid() anot
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)



# class CommentDetailAPIView(RetrieveAPIView):
#     queryset = CommentModel.objects.all()
#     serializer_class = CommentDetailSerializer
#     # in default, urls.py will lookup to the pk or id field.
#     # lookup_field = 'slug' (if you have a slug field instead of pk )
#
# # Update & Destroy Mixins
# # https://www.youtube.com/watch?v=DX3ekF1Xx8U&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS&index=22
# class CommentUpdateAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
#     queryset = CommentModel.objects.filter(id__gte=0)
#     serializer_class = CommentUpdateSerializer
#
#     # "def put()" method is the built-in method for all the APIView that handle any kind of put(update/edit)
#     def put(self, request, *args, **kwargs):
#         #self.update is come from UpdateModelMixin
#         return self.update(request, *args, **kwargs)
#
#     # "def delete()" is the built-in method for all the APIView that handle specific for delete(destroy)
#     def delete(self, request, *args, **kwargs):
#         #self.destroy is come from DestroyModelMixin
#         return self.destroy(request, *args, **kwargs)
