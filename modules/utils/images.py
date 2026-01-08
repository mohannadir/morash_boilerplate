from PIL import Image
from django.db.models.fields.files import ImageFieldFile as DjangoImageFieldFile
from django.core.files.base import ContentFile
import qrcode
from typing import Optional, Union
import base64
import io
import requests
import os
from io import BytesIO
from django.contrib.staticfiles import finders

def remove_whitespace_from_image(image: Optional[Union[str, DjangoImageFieldFile]]) -> Image:
    """ Remove whitespace from image and save it to the same path. 
    
        :param image_path: path to image
        :param save_modified_image: whether to save the modified image to the same path
        :return: image without whitespace
        :rtype: Image
    """

    if isinstance(image, DjangoImageFieldFile):
        image_path = image.path
    else:
        image_path = image
    
    image_obj = Image.open(image_path)

    # remove whitespace
    image_without_whitespace = image_obj.crop(image_obj.getbbox())
    image_without_whitespace.save(image_path)

    return image_without_whitespace

def compress_image(image: Optional[Union[str, DjangoImageFieldFile]], max_size: int, scale: int) -> None:
    """ Compress image and save it to the same path.
        
        This function will compress the image until it is smaller than max_size. 
        It will do so by resizing the image by the given scale until it is smaller than max_size.
    
        :param image: path to image or DjangoImageFieldFile
        :param max_size: max size in bytes
        :param scale: scale to resize the image by
    """

    if isinstance(image, DjangoImageFieldFile):
        image_path = image.path
    else:
        image_path = image

    image_obj = Image.open(image_path)

    # if the current image is already smaller than the max_size, don't compress it
    current_file_size = os.path.getsize(image_path)
    if current_file_size <= max_size:
        return

    # compress the image. If max_size is given, compress the image until it is smaller than max_size
    current_size = image_obj.size

    image_obj = image_obj.convert('RGB')

    while True:
        current_size = (int(current_size[0] * scale), int(current_size[1] * scale))
        resized_file = image_obj.resize(current_size, Image.LANCZOS)

        with io.BytesIO() as file_bytes:
            resized_file.save(file_bytes, optimize=True, quality=95, format='jpeg')

            if file_bytes.tell() <= max_size:
                file_bytes.seek(0, 0)
                with open(image_path, 'wb') as f_output:
                    f_output.write(file_bytes.read())
                break


def crop_image(image: Optional[Union[str, DjangoImageFieldFile]], coords: tuple) -> Image:
    """ Crop image with given coords and save it to the same path. 
    
        :param image_path: path to image
        :param coords: tuple of coords (x1, y1, x2, y2)
        :return: cropped image
        :rtype: Image
        :raises: None if coords are too big for image
    """

    if isinstance(image, DjangoImageFieldFile):
        image_path = image.path
    else:
        image_path = image
    
    image_obj = Image.open(image_path)

    # check if coords are not too big for image
    width, height = image_obj.size
    if coords[2] > width or coords[3] > height:
        return None
    
    cropped_image = image_obj.crop(coords)
    cropped_image.save(image_path)

    return cropped_image

def crop_image_width(image: Optional[Union[str, DjangoImageFieldFile]], width: int) -> Image:
    """ Crop image with given width and save it to the same path. 
    
        :param image_path: path to image
        :param width: width of cropped image
        :return: cropped image
        :rtype: Image
        :raises: None if width is too big for image
    """

    if isinstance(image, DjangoImageFieldFile):
        image_path = image.path
    else:
        image_path = image

    image_obj = Image.open(image_path)

    # check if width is not too big for image
    image_width, image_height = image_obj.size
    if width > image_width:
        return None

    # calculate coords
    x1 = (image_width - width) // 2
    y1 = 0
    x2 = x1 + width
    y2 = image_height

    cropped_image = image_obj.crop((x1, y1, x2, y2))
    cropped_image.save(image_path)

    return cropped_image

def crop_image_height(image: Optional[Union[str, DjangoImageFieldFile]], height: int) -> Image:
    """ Crop image with given height and save it to the same path. 
    
        :param image_path: path to image
        :param height: height of cropped image
        :return: cropped image
        :rtype: Image
        :raises: None if height is too big for image
    """

    if isinstance(image, DjangoImageFieldFile):
        image_path = image.path
    else:
        image_path = image
    
    image_obj = Image.open(image_path)

    # check if height is not too big for image
    image_width, image_height = image_obj.size
    if height > image_height:
        return None

    # calculate coords
    x1 = 0
    y1 = (image_height - height) // 2
    x2 = image_width
    y2 = y1 + height

    cropped_image = image_obj.crop((x1, y1, x2, y2))
    cropped_image.save(image_path)

    return cropped_image
    
def get_image_from_datauri(datauri: str, filename: str) -> ContentFile:
    """ Returns an image from a datauri with the given filename. Returns the image as a ContentFile.
    
        :param datauri: datauri to get image from
        :type datauri: str
        :param filename: filename to save image to
        :type filename: str
        :return: image
        :rtype: ContentFile
    """

    format, imgstr = datauri.split(';base64,')
    ext = format.split('/')[-1]
    return ContentFile(base64.b64decode(imgstr), name=f'{filename}.{ext}')

def convert_image_to_datauri(image: DjangoImageFieldFile) -> str:
    """ Returns a datauri from a DjangoImageFieldFile.
    
        :param image: image to convert
        :type image: DjangoImageFieldFile
        :return: datauri
        :rtype: str
    """

    file_extension = image.file.name.split('.')[-1].lower()

    if file_extension == 'png':
        content_type = 'image/png'
    elif file_extension in ['jpg', 'jpeg']:
        content_type = 'image/jpeg'
    elif file_extension == 'webp':
        content_type = 'image/webp'
    else:
        content_type = f'image/{file_extension}'

    return f'data:{content_type};base64,{base64.b64encode(image.read()).decode()}'

def get_image_from_url_and_convert_to_b64(url: str) -> str:
    """ Returns a base64 encoded image from a url.
    
        :param url: url to get image from
        :type url: str
        :return: base64 encoded image
        :rtype: str
    """

    image = Image.open(io.BytesIO(requests.get(url).content))
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()