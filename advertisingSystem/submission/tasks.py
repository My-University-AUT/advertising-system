from celery import shared_task, Task
from django.db import transaction
from utils.utils import getImageUrl
import requests
import urllib.parse
from advertisingSystem.settings import IMAGE_PROCESS_BASE_URL, IMAGE_PROCESS_BASIC_AUTH
from submission.models import Advertise


class TransactionAwareTask(Task):
    """
    Task class which is aware of django db transactions and only executes tasks
    after transaction has been committed
    """

    abstract = True

    def apply_async(self, *args, **kwargs):
        """
        Unlike the default task in celery, this task does not return an async
        result
        """
        transaction.on_commit(
            lambda: super(TransactionAwareTask, self).apply_async(*args, **kwargs)
        )


@shared_task(time_limit=60, base=TransactionAwareTask, bind=True)
def processImage(self, imageId, advertiseId):
    print("hello celery", imageId, advertiseId)
    imageUrl = getImageUrl(imageId)
    print(imageUrl)
    
    encodedUrl = urllib.parse.quote_plus(imageUrl)
    url = f"{IMAGE_PROCESS_BASE_URL}tags?image_url={encodedUrl}"

    payload={}
    headers = {
    'Authorization': f'Basic {IMAGE_PROCESS_BASIC_AUTH}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print("===========================")
    print("image gaaaa", response.json())
    imageTags = response.json()['result']['tags']

    print(type(imageTags))
    if isinstance(imageTags, list):
        result = next(filter(lambda x: x['confidence'] > 50 and x['tag']['en'] == 'vehicle', imageTags), {})
        
        category = None
        status = 0
        if result:
            print("here is result", result)
            category = result['tag']['en']
            # accepted status
            status = 1
        else:
            # rejected status
            status = 2
            print("result is empty")
        with transaction.atomic():
            advertise = Advertise.objects.get(id=advertiseId)
            advertise.category = category
            advertise.status = status
            advertise.save()
            
            print("DONE!")

        
#  celery -A mysite worker --loglevel=INFO --concurrency=8 -n worker1@%h
