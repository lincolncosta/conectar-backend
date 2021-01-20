from pathlib import Path
from os import chdir
from PIL import Image

import numpy as np
from io import BytesIO

from core.security.passwords import get_password_hash

path = Path("uploads/")


path.mkdir(parents=True, exist_ok=True)

def store_image(image, image_id):
    name = get_password_hash(image_id) + ".png"
    image_name = name.replace('/', '')
    try:
        pil_image = np.array(Image.open(BytesIO(image)))
        Image.fromarray(pil_image).save(path / f"{image_name}")

        return image_name
            
    except Exception as e:
        print(f'Exception from store_image {e}')
