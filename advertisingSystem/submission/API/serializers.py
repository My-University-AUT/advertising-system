from django.db.models import Q
from rest_framework import serializers
from submission.models import Advertise
from django.db import transaction
from utils.utils import uploadToCloud
from submission.tasks import processImage
from utils.utils import getImageUrl
class AdvertiseSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True, write_only=True)

    imageLink = serializers.SerializerMethodField(method_name='get_image_link', read_only=True)

    def get_image_link(self, instance):
        imageUrl = getImageUrl(instance.imageId)
        return imageUrl
        
    class Meta:
        model = Advertise
        fields = ['description', 'status', 'image', 'email', 'id', 'category', 'imageLink']
        extra_kwargs = {
            'status': {
                "read_only": True
            },
            'description': {
                'required': True,
                'write_only': False
            },
            'email': {
                'required': True,
                'write_only': False
            },
            'id': {
                'read_only': True
            },
            'category': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        with transaction.atomic():
            imageToUpload = validated_data.pop('image')
            createdAdvertise = Advertise.objects.create(**validated_data)

            # upload image to aws object storage
            # then save the field id to the createdAdvertise
            imageId = f'{createdAdvertise.id}_{imageToUpload.name}'
            img = imageToUpload.file
            createdAdvertise.imageId = imageId
            createdAdvertise.save()
            uploadToCloud(img, imageId)
            processImage.delay(imageId, createdAdvertise.id)

            return  createdAdvertise

    def update(self, instance, validated_data):
        pass
