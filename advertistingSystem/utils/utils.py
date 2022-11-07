import boto3
import logging
from botocore.exceptions import ClientError
from advertistingSystem.settings import AWS_BASE_URL, AWS_ACCESS_KEY, AWS_SECRET_KEY, OBJECT_STORAGE_BUCKET_NAME


def uploadToCloud(image, imageId):

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url=AWS_BASE_URL,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

    except Exception as exc:
        logging.error(exc)
    else:
        try:
            bucket = s3_resource.Bucket(OBJECT_STORAGE_BUCKET_NAME)
            bucket.put_object(
                ACL='private',
                Body=image,
                Key=imageId
            )
        except ClientError as e:
            logging.error(e)


def getImageUrl(imageId):
    try:
        s3_client = boto3.client(
            's3',
            endpoint_url=AWS_BASE_URL,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

    except Exception as exc:
        logging.error(exc)
    else:
        try:
            bucket = OBJECT_STORAGE_BUCKET_NAME
            object_name = imageId

            response = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket,
                    'Key': object_name
                },
                ExpiresIn=3600
            )

            return response
        except ClientError as e:
            logging.error(e)