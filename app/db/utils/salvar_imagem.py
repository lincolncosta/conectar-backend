from pathlib import Path
import os
from PIL import Image

import numpy as np
from io import BytesIO
import uuid


if not os.getenv("DEV_ENV"):
    import boto3
    from botocore.exceptions import ClientError
    import logging

def upload_object(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
      
    return True

if not os.getenv("DEV_ENV"):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ID"),
        aws_secret_access_key=os.getenv("AWS_KEY")
    )

IMAGE_PATH = "uploads/"
PDF_PATH = "PDF/"
path = Path(IMAGE_PATH)
path.mkdir(parents=True, exist_ok=True)

def store_image(image):
    image_name = str(uuid.uuid4().hex) + ".png"
    try:
       
        pil_image = np.array(Image.open(BytesIO(image)))
        Image.fromarray(pil_image).save(path / f"{image_name}")

        if not os.getenv("DEV_ENV"):
            upload_object(IMAGE_PATH + image_name , 'conectar')
        os.remove(IMAGE_PATH + image_name)        
        return image_name
            
    except Exception as e:
        print(f'Exception from store_image {e}')

def delete_file(image_name):
    try:
        if not os.getenv("DEV_ENV"):
            extension = image_name.split(".")[-1]
            if extension != 'pdf':
                s3_client.delete_object(Bucket='conectar', Key=IMAGE_PATH + image_name)
            else: 
                s3_client.delete_object(Bucket='conectar', Key=PDF_PATH + image_name)
        return True

    except Exception as e:
        return False
