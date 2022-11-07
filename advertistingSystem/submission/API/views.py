from rest_framework import mixins
from rest_framework import viewsets
from submission.API.serializers import AdvertiseSerializer

class SubmissionAPIView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    serializer_class = AdvertiseSerializer
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        # return Response("hello")
