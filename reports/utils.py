import base64
import uuid
from django.core.files.base import ContentFile


def is_ajax(meta):
    if 'HTTP_X_REQUESTED_WITH' not in meta:
        return False

    if meta['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
        return True

    return False

def get_report_image(data):
    _, str_image = data.split(';base64')
    decoded_img = base64.b64decode(str_image)
    img_name = str(uuid.uuid4())[:10]+'.png'
    data = ContentFile(decoded_img, name=img_name)
    return data
