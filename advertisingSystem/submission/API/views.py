from rest_framework import mixins
from rest_framework import viewsets
from submission.API.serializers import AdvertiseSerializer
from submission.models import Advertise
from rest_framework.exceptions import ValidationError
class SubmissionAPIView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    serializer_class = AdvertiseSerializer

    def get_object(self):
        id = self.kwargs['id']
        # status 1 is for accepted advertise
        try:
            advertise = Advertise.objects.get(id=id)

            if advertise.status == 2:
                raise ValidationError('advertise is rejected')
            elif advertise.status == 1:
                return advertise
            else:
                raise ValidationError('adverstise is not accepted yet')
        except Advertise.DoesNotExist:
            raise ValidationError('advertise does not exist')

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        # return Response("hello")
