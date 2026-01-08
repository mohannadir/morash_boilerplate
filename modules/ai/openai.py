from openai import OpenAI
from django.conf import settings
from typing import Literal
from modules.utils.images import get_image_from_url_and_convert_to_b64

def generate_image(prompt: str, size: Literal["1024x1024", "1024x1792", "1792x1024"], quality: Literal["standard", "hd"] = 'standard') -> str:
    """ Generates an image using OpenAI's DALL-E model. 
    
        :param prompt: The prompt to generate the image from.
        :type prompt: str
        :param size: The size of the image to generate.
        :type size: Literal["1024x1024", "1024x1792", "1792x1024"]
        :param quality: The quality of the image to generate.
        :type quality: Literal["standard", "hd"]
        :return: The base64 encoded image.
        :rtype: str
    """

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality=quality,
        n=1,
    )

    # OpenAI also provides the base64 directly, but these are usually around 7MB.
    # This is too big to use in a form field, so we'll just use the url and convert it to base64 ourselves
    # This will result in a much smaller base64 string
    url = response.data[0].url
    return get_image_from_url_and_convert_to_b64(url)