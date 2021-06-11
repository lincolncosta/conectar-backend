from pathlib import Path
from os import chdir, getenv
from PIL import Image

import numpy as np
from io import BytesIO
import uuid

from core.security.passwords import get_password_hash

import boto3
from botocore.exceptions import ClientError
import logging

def upload_object(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
      
    return True

s3_client = boto3.client(
    's3',
    aws_access_key_id=getenv("AWS_ID"),
    aws_secret_access_key=getenv("AWS_KEY")
)

IMAGE_PATH = "uploads/"
path = Path(IMAGE_PATH)

path.mkdir(parents=True, exist_ok=True)

def store_image(image):
    image_name = str(uuid.uuid4().hex) + ".png"
    try:
        pil_image = np.array(Image.open(BytesIO(image)))
        Image.fromarray(pil_image).save(path / f"{image_name}")

        upload_object(IMAGE_PATH + image_name , 'conectar')
        
        return image_name
            
    except Exception as e:
        print(f'Exception from store_image {e}')

def delete_image(image_name):
    try:
        s3_client.delete_file(Bucket='conectar', Key=IMAGE_PATH + image_name)
    
        return True

    except Exception as e:
        return False
